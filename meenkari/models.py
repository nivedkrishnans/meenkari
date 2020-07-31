from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    #game takes place here
    game_id = models.CharField(max_length=127, null=False, blank=True)
    #players lobby here
    lobby_id = models.CharField(max_length=127, null=False, blank=True)
    game_name = models.CharField(default="Unnamed Game", max_length=32, null=False, blank=False)
    #determines whether or not the game appears in the join page
    game_privacy = models.CharField(default="public", max_length=10, choices=(("public","Public"),("private","Private"),))
    game_status = models.CharField(default="empty", max_length=10, choices=(("empty","Empty"),("united","United"),("started","Started"),("over","Over"),("stopped","Stopped")))
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    lastmodify_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    #p0 shall be the current player
    p0 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='p0', null=True, blank=True)
    #p1 shall be the host.
    p1 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='p1', null=True, blank=True)
    p2 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='p2', null=True, blank=True)
    p3 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='p3', null=True, blank=True)
    p4 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='p4', null=True, blank=True)
    p5 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='p5', null=True, blank=True)
    p6 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='p6', null=True, blank=True)
    log =  models.TextField(blank=True)
    p1_hand =  models.TextField(blank=True)
    p2_hand =  models.TextField(blank=True)
    p3_hand =  models.TextField(blank=True)
    p4_hand =  models.TextField(blank=True)
    p5_hand =  models.TextField(blank=True)
    p6_hand =  models.TextField(blank=True)
    team_1_status = models.CharField(max_length=40, null=False, blank=True)
    team_2_status = models.CharField(max_length=40, null=False, blank=True)

    def __str__(self):
        return self.game_name

class Lobby(models.Model):
    game = models.OneToOneField(Game, on_delete=models.SET_NULL, related_name='lobby', null=True, blank=True)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    players = models.ManyToManyField(User, related_name='lobby_history',  blank=True)

    def __str__(self):
        return str(self.game)
