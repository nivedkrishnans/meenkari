from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    #game takes place here
    game_id = models.CharField(max_length=127, null=False, blank=True)
    #players unite here
    unite_id = models.CharField(max_length=127, null=False, blank=True)
    game_name = models.CharField(default="Unnamed Game", max_length=32, null=False, blank=False)
    #determines whether or not the game appears in the join page
    game_privacy = models.CharField(default="public", max_length=10, choices=(("public","Public"),("private","Private"),))
    game_status = models.CharField(default="empty", max_length=10, choices=(("empty","Empty"),("united","United"),("started","Started"),("over","Over"),("stopped","Stopped")))
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    lastmodify_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    #player_11 shall be the host
    player_11 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='player_11', null=True, blank=True)
    player_12 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='player_12', null=True, blank=True)
    player_13 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='player_13', null=True, blank=True)
    player_21 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='player_21', null=True, blank=True)
    player_22 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='player_22', null=True, blank=True)
    player_23 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='player_23', null=True, blank=True)
    log =  models.TextField(blank=True)
    player_11_hand =  models.TextField(blank=True)
    player_12_hand =  models.TextField(blank=True)
    player_13_hand =  models.TextField(blank=True)
    player_21_hand =  models.TextField(blank=True)
    player_22_hand =  models.TextField(blank=True)
    player_23_hand =  models.TextField(blank=True)
    team_1_status = models.CharField(max_length=40, null=False, blank=True)
    team_2_status = models.CharField(max_length=40, null=False, blank=True)

    def __str__(self):
        return self.game_name

class UniteQueue(models.Model):
    game = models.OneToOneField(Game, on_delete=models.SET_NULL, related_name='unite_queue', null=True, blank=True)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    players = models.ManyToManyField(User, related_name='unite_queue_history',  blank=True)

    def __str__(self):
        return str(self.game)
