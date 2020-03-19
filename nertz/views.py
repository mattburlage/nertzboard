from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from nertz.models import Room, Game, Hand, Round
from .serializers import UserSerializer, UserSerializerWithToken, RoomSerializer, GameSerializer, CreateHandSerializer, \
    UserSerializerSignup


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class CurrentRoom(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(pk=user.rooms.first().id)


@api_view(['GET'])
def current_room_data(request):
    room = Room.objects.get(pk=request.user.rooms.first().id)
    game = room.games.last()
    curround = len(game.rounds.all())

    room_data = {
        'name': room.name,
        'game': game.id,
        'round': curround,
    }
    return Response(room_data)


@api_view(['GET'])
def current_game_data(request):
    room = Room.objects.get(pk=request.user.rooms.first().id)
    game = room.games.last()
    game_hands = Hand.objects.filter(round__game=game)
    curround = len(game.rounds.all())

    game_data = []
    max_rounds = 0
    for player in game.players.all():

        player_hands = game_hands.filter(player=player)

        points = player_hands.aggregate(Sum('points'))['points__sum'] or 0
        nertz = player_hands.aggregate(Sum('nertz'))['nertz__sum'] or 0
        score = points - (nertz * 2)

        rounds = len(player_hands)
        if rounds > max_rounds:
            max_rounds = rounds

        game_data.append({
            'id': player.id,
            'name': player.get_full_name(),
            'username': player.get_username(),
            'score': score,
            'rounds': rounds,
        })

    room_data = {
        'name': room.name,
        'game': game.id,
        'curround': curround,
        'max_rounds': max_rounds,
    }

    game_data = {
        'room_data': room_data,
        'rounds': sorted(game_data, key=find_score, reverse=True),
    }

    return Response(game_data)


def find_score(element):
    return element['score']


class CurrentGame(generics.ListAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        user = self.request.user

        return Game.objects.filter(pk=user.rooms.first().games.last().id)


def add_to_room(user, room_name):
    try:
        room = Room.objects.get(name=room_name)
        room.games.first().players.add(user)
    except Room.DoesNotExist:
        room = Room.objects.create(name=room_name)
        game = Game.objects.create(room=room)
        game.players.add(user)
        Round.objects.create(game=game)

    room.members.add(user)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        room = request.data['roomName']
        serializer = UserSerializerSignup(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            add_to_room(user, room)

            data_serializer = UserSerializerWithToken(user)

            return Response(data_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def check_for_new_round(game, create=True):
    rounds = game.rounds.all()
    hands = rounds.last().hands.all()

    if len(hands) != len(game.players.all()):
        return False

    if create:
        new_round = Round(
            game=game,
        )
        new_round.save()
        return new_round

    return True


class CreateHand(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = CreateHandSerializer(data=request.data)
        usr = request.user
        room = usr.rooms.first()
        game = room.curgame
        max_rounds = len(game.rounds.all())
        curround = game.curround
        usr_rounds = len(usr.hands.filter(round__game=game))

        if serializer.is_valid() and usr_rounds == max_rounds - 1:
            data = serializer.data
            new_hand = Hand(
                player=request.user,
                round=curround,
                nertz=data['nertz'],
                points=data['points'],
            )
            new_hand.save()

            check_for_new_round(game)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif serializer.is_valid() and not usr_rounds == max_rounds - 1:

            if check_for_new_round(game, create=False):
                new_round = check_for_new_round(game)

                data = serializer.data
                new_hand = Hand(
                    player=request.user,
                    round=new_round,
                    nertz=data['nertz'],
                    points=data['points'],
                )
                new_hand.save()

                check_for_new_round(game)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                error_data = {
                    'message': 'Hand already submitted. Please wait for new round.',
                    'usr_rounds': usr_rounds,
                    'max_rounds': max_rounds,
                }

            return Response(error_data, status=status.HTTP_409_CONFLICT)
        elif not serializer.is_valid():
            check_for_new_round(game)

            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def new_game(request):
    if not request.user.is_authenticated:
        return Response({'message': 'no'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        create_new_game(request.user)
    except:
        return Response({'message': 'no'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'ok'}, status=status.HTTP_200_OK)


def create_new_game(user):
    room = user.rooms.first()
    game = Game.objects.create(room=room)
    for uzr in room.members.all():
        game.players.add(uzr)
    Round.objects.create(game=game)
