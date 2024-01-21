from django.db import models
import uuid

class GameMember(models.Model):
    id = models.CharField(max_length=100, primary_key=True,default=uuid.uuid4)
    name = models.CharField(max_length=100)
    room = models.ForeignKey("GameRoom",on_delete=models.CASCADE,related_name="members")

class GameRoom(models.Model):
    id = models.CharField(max_length=100, primary_key=True,default=uuid.uuid4)
    code = models.CharField(max_length=5)
    members_count = models.IntegerField(default=0)
    game = models.CharField(max_length=5,default="none")

class Bingo(models.Model):
    id = models.CharField(max_length=100, primary_key=True,default=uuid.uuid4)
    room = models.ForeignKey(GameRoom,on_delete=models.CASCADE)
    used_numbers = models.JSONField(default=list)
    winner = models.ForeignKey(GameMember,on_delete=models.CASCADE,null=True)
    next_move = models.ForeignKey(GameMember,on_delete=models.CASCADE,null=True,related_name="next_move")
    game_over = models.BooleanField(default=False)