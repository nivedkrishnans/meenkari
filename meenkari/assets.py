from django.utils import timezone
from .models import *
import string
import random
import json
from asgiref.sync import async_to_sync
import channels.layers
from django.conf import settings

delimiter = ","
game_id_size = 32
unite_id_size = 32

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



def assign_id(thisgame):    #the argument is a game instance
    all_game_ids = Game.objects.all().values('game_id')
    all_unite_ids = Game.objects.all().values('unite_id')

    #choosing game_id
    random_id_chosen = False
    while not random_id_chosen:
      random_id = random_string_generator(game_id_size)
      if (random_id not in all_game_ids):
        random_id_chosen = True
        thisgame.game_id = random_id

    #choosing unite_id
    random_id_chosen = False
    while not random_id_chosen:
      random_id = random_string_generator(unite_id_size)
      if (random_id not in all_unite_ids):
        random_id_chosen = True
        thisgame.unite_id = random_id




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



def host_queue_update(thisgame):
    #this function updates the host about the players in the queue
    this_group_name = "unite-" + thisgame.unite_id + "-host"
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        this_group_name, {
            "type": 'queue_update',
            "content": json.dumps(unite_queue_json(thisgame)),
        })


def unite_queue_json(thisgame):
    #this function generates the present player queue inorder to show the host
    this_queue = list(thisgame.unite_queue.players.all().values_list('username', flat=True))
    this_queue_json = {
        "type": 'queue_update',
        'time': str(timezone.now()),
        'unite_id': thisgame.unite_id,
        'queue': this_queue,
    }
    return this_queue_json


def unite_queue_update(thisgame):
    #this function updates the non-host that the players have been chosen. they players will be asked to reload the page
    this_group_name = "unite-" + thisgame.unite_id + "-" + 'queue'
    unite_queue_update = {
        "type": 'queue_update',
        'time': str(timezone.now()),
        'unite_id': thisgame.unite_id,
    }
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        this_group_name, {
            "type": 'queue_update',
            "content": json.dumps(unite_queue_update),
        })




















#test and trial functions

def game_details_generator(thisgame): #returns the game details as json, which is needed only once during the game
    game_details = {'game_name':thisgame.game_name,'game_id':thisgame.game_id,'game_status':thisgame.game_status,
                    'p11':{'id':thisgame.p1,'img':thisgame.p1_image,},
                    'p12':{'id':thisgame.p2,'img':thisgame.p2_image,},
                    'p13':{'id':thisgame.p3,'img':thisgame.p3_image,},
                    'p21':{'id':thisgame.p4,'img':thisgame.p4_image,},
                    'p22':{'id':thisgame.p5,'img':thisgame.p5_image,},
                    'p23':{'id':thisgame.p6,'img':thisgame.p6_image,},
    }
    return game_details

def current_status_generator(thisgame): #returns the game status as json, which is needed for every move in the game
    current_status ={'time': str(timezone.now()),
                    'p11hand':thisgame.p1_hand,
                    'p12hand':thisgame.p2_hand,
                    'p13hand':thisgame.p3_hand,
                    'p21hand':thisgame.p6_hand,
                    'p22hand':thisgame.p5_hand,
                    'p23hand':thisgame.p6_hand,
                    't1':thisgame.team_1_status,
                    't2':thisgame.team_2_status,
                }
    return current_status



def broadcast_live(info_json,game_id,username):
    this_group_name = game_id + '-' + username
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        this_group_name, {
            "type": 'game_update',
            "content": json.dumps(info_json),
        })








#alternate function, ignore this
def shuffle_cards1():
    shuffling = random.sample(newdeck)
    shuffleddeck = (
            delimiter.join(shuffling[0:9]),
            delimiter.join(shuffling[9:18]),
            delimiter.join(shuffling[18:27]),
            delimiter.join(shuffling[27:36]),
            delimiter.join(shuffling[36:45]),
            delimiter.join(shuffling[45:54]),
    )
    return shuffleddeck
