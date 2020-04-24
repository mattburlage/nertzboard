from rest_framework import serializers, relations
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User

from nertz.models import Room, Game, Round, Hand


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'is_superuser', 'rooms')


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password', 'is_superuser', 'rooms')


class UserSerializerSignup(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password', 'first_name')


class HandSerializer(serializers.ModelSerializer):
    player = relations.StringRelatedField(many=False)

    class Meta:
        model = Hand
        fields = ('id', 'score', 'player')


class CreateHandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hand
        fields = ('nertz', 'points')


class RoundSerializer(serializers.ModelSerializer):
    hands = HandSerializer(many=True)

    class Meta:
        model = Round
        fields = ('id', 'hands')


class GameSerializer(serializers.ModelSerializer):
    rounds = RoundSerializer(many=True)

    class Meta:
        model = Game
        fields = ('id', 'room', 'players', 'rounds')


class UserGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', )


class RoomSerializer(serializers.ModelSerializer):
    members = relations.StringRelatedField(many=True)

    class Meta:
        model = Room
        fields = ('id', 'name', 'members')


