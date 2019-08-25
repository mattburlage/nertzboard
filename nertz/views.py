from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from nertz.models import Room, Game, Hand
from .serializers import UserSerializer, UserSerializerWithToken, RoomSerializer, GameSerializer


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

        points = player_hands.aggregate(Sum('points'))['points__sum']
        nertz = player_hands.aggregate(Sum('nertz'))['nertz__sum']
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


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)