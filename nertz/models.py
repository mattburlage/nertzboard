from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=64)
    members = models.ManyToManyField(User, related_name='rooms')

    def __str__(self):
        return self.name


class Game(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='games')
    players = models.ManyToManyField(User, related_name='games')

    def __str__(self):
        return f'Game {self.pk} ({self.room.name})'


class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='rounds')

    def __str__(self):
        return f'Round {self.pk} (Game {self.game_id} in {self.game.room.name})'


class Hand(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='hands')
    player = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='hands')
    nertz = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def score(self):
        return self.points - (self.nertz * 2)

    def __str__(self):
        return f'Hand {self.id} for {self.player.username} (Round {self.round_id}, ' \
               f'Game {self.round.game_id}, Room {self.round.game.room.name})'
