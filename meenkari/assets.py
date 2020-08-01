from django.utils import timezone
#from datetime import datetime
from .models import *
import string
import random
import json
from asgiref.sync import async_to_sync
import channels.layers
from django.conf import settings





#IMPORTANT: For all jsons to be sent to the client, use double quotes inside and single quotes at the very outside


delimiter = ","
game_id_size = 32
lobby_id_size = 32

def random_string_generator(size):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k = size))



newdeck = [
    #the 9 half-suits and their 6 cards
    "11", "12", "13", "14", "15", "16",
    "21", "22", "23", "24", "25", "26",
    "31", "32", "33", "34", "35", "36",
    "41", "42", "43", "44", "45", "46",
    "51", "52", "53", "54", "55", "56",
    "61", "62", "63", "64", "65", "66",
    "71", "72", "73", "74", "75", "76",
    "81", "82", "83", "84", "85", "86",
    "91", "92", "93", "94", "95", "96",
]


def shuffle_cards(thisgame): #the argument is a game instance
    shuffleddeck= random.sample(newdeck, k=54)
    thisgame.p1_hand =  delimiter.join(shuffleddeck[0:9]) + delimiter
    thisgame.p2_hand =  delimiter.join(shuffleddeck[9:18]) + delimiter
    thisgame.p3_hand =  delimiter.join(shuffleddeck[18:27]) + delimiter
    thisgame.p4_hand =  delimiter.join(shuffleddeck[27:36]) + delimiter
    thisgame.p5_hand =  delimiter.join(shuffleddeck[36:45]) + delimiter
    thisgame.p6_hand =  delimiter.join(shuffleddeck[45:54]) + delimiter
    thisgame.save();



def assign_id(thisgame):
    #this function assigns random strings as game_id and lobby_id for the game instance passed as argument.
    #the length of the random strings is defined by game_id_size and lobby_id_size declared globally
    all_game_ids = Game.objects.all().values('game_id')
    all_lobby_ids = Game.objects.all().values('lobby_id')

    #choosing game_id
    random_id_chosen = False
    while not random_id_chosen:
      random_id = random_string_generator(game_id_size)
      if (random_id not in all_game_ids):
        random_id_chosen = True
        thisgame.game_id = random_id

    #choosing lobby_id
    random_id_chosen = False
    while not random_id_chosen:
      random_id = random_string_generator(lobby_id_size)
      if (random_id not in all_lobby_ids):
        random_id_chosen = True
        thisgame.lobby_id = random_id




def is_player(thisuser,thisgame):
    player_list = {
        thisgame.p1,
        thisgame.p2,
        thisgame.p3,
        thisgame.p4,
        thisgame.p5,
        thisgame.p6,
    }
    if thisuser in player_list:
        return True
    else:
        return False


def is_host(thisuser,thisgame):
    return (thisuser == thisgame.p1)



def host_lobby_update(thisgame):
    #this function updates the host about the players in the queue
    this_group_name = "lobby-" + thisgame.lobby_id + "-host"
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        this_group_name, {
            "type": 'lobby_update',
            "content": json.dumps(lobby_json(thisgame)),
        })


def lobby_json(thisgame):
    #this function generates the present player queue inorder to show the host
    this_queue = list(thisgame.lobby.players.all().values_list('username', flat=True))
    this_queue_json = {
        "type": 'lobby_update',
        'time': str(timezone.now()),
        'lobby_id': thisgame.lobby_id,
        'queue': this_queue,
    }
    return this_queue_json


def player_lobby_update(thisgame):
    #this function updates the non-host that the players have been chosen. they players will be asked to reload the page
    this_group_name = "lobby-" + thisgame.lobby_id + "-" + 'queue'
    lobby_update = {
        "type": 'lobby_update',
    }
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        this_group_name, {
            "type": 'lobby_update',
            "content": json.dumps(lobby_update),
        })



def game_status_json(thisuser,thisgame,message):
    #arguments are a user instance and a game instance, and a string/integer which carries some message to the client
    hand_lengths = [
        int(len(thisgame.p1_hand)/3),
        int(len(thisgame.p2_hand)/3),
        int(len(thisgame.p3_hand)/3),
        int(len(thisgame.p4_hand)/3),
        int(len(thisgame.p5_hand)/3),
        int(len(thisgame.p6_hand)/3),
    ]
    game_status_json = {
        "ty":"gsj",
        "ts": str(timezone.now()),
        "hl": hand_lengths,
        "my": player_status_finder(thisuser,thisgame),
        "te": [thisgame.team_1_status,thisgame.team_2_status],
        "p0": str(thisgame.p1),
        "me": message,
    }
    return json.dumps(game_status_json)



def game_info_json(thisgame):
    game_info = {
        "pl":[str(thisgame.p1), str(thisgame.p2), str(thisgame.p3), str(thisgame.p4), str(thisgame.p5), str(thisgame.p6),],
        "na": thisgame.game_name,
        "pr": thisgame.game_privacy,
        "ts": str(thisgame.create_time),
    }
    return json.dumps(game_info)



def player_status_finder(thisuser,thisgame):
    #finds the number (1-6) and the hand of a user in a game
    if thisgame.p1 == thisuser:
        return [1, thisgame.p1_hand]
    elif thisgame.p2 == thisuser:
        return [2, thisgame.p2_hand]
    elif thisgame.p3 == thisuser:
        return [3, thisgame.p3_hand]
    elif thisgame.p4 == thisuser:
        return [4, thisgame.p4_hand]
    elif thisgame.p5 == thisuser:
        return [5, thisgame.p5_hand]
    elif thisgame.p6 == thisuser:
        return [6, thisgame.p6_hand]
    else:
        #zero means the player isn't a part of the game
        return [0, "error"]

def game_status_update(thisuser,thisgame,message):
    #this function sends the game_status_json to the players on the game page in an active game
    this_group_name = "game-" + thisgame.game_id + "-" + str(thisuser)
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        this_group_name, {
            "type": 'game_update',
            "content": json.dumps(game_status_json(thisuser,thisgame,message)),
        })



def tester_sender(group,message):
    #this function sends the message from the tester to the given group
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {
            "type": 'game_update',
            "content": json.dumps(message),
        })
