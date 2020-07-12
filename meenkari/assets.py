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

newdeck = [
    #the 9 half-suits and their 6 cards
    "a1", "a2", "a3", "a4", "a5", "a6",
    "b1", "b2", "b3", "b4", "b5", "b6",
    "c1", "c2", "c3", "c4", "c5", "c6",
    "d1", "d2", "d3", "d4", "d5", "d6",
    "e1", "e2", "e3", "e4", "e5", "e6",
    "f1", "f2", "f3", "f4", "f5", "f6",
    "g1", "g2", "g3", "g4", "g5", "g6",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "i1", "i2", "i3", "i4", "i5", "i6",
]

#alternative deck notations if needed
newdeck_alternative = [
    "ls02", "ls03", "ls04", "ls05", "ls06", "ls07", "jos8", "hs09", "hs10", "hs_j", "hs_q", "hs_k", "hs_a",
    "lc02", "lc03", "lc04", "lc05", "lc06", "lc07", "joc8", "hc09", "hc10", "hc_j", "hc_q", "hc_k", "hc_a",
    "lh02", "lh03", "lh04", "lh05", "lh06", "lh07", "joh8", "hh09", "hh10", "hh_j", "hh_q", "hh_k", "hh_a",
    "ld02", "ld03", "ld04", "ld05", "ld06", "ld07", "jod8", "hd09", "hd10", "hd_j", "hd_q", "hd_k", "hd_a",
    "jo_b", "jo_w",
]



def shuffle_cards(thisgame): #the argument is a game instance
    shuffleddeck= random.sample(newdeck, k=54)
    thisgame.player_11_hand =  delimiter.join(shuffleddeck[0:9]) + delimiter
    thisgame.player_12_hand =  delimiter.join(shuffleddeck[9:18]) + delimiter
    thisgame.player_13_hand =  delimiter.join(shuffleddeck[18:27]) + delimiter
    thisgame.player_21_hand =  delimiter.join(shuffleddeck[27:36]) + delimiter
    thisgame.player_22_hand =  delimiter.join(shuffleddeck[36:45]) + delimiter
    thisgame.player_23_hand =  delimiter.join(shuffleddeck[45:54]) + delimiter
    thisgame.save();


def random_string_generator(size):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k = size))

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
        thisgame.player_11,
        thisgame.player_12,
        thisgame.player_13,
        thisgame.player_21,
        thisgame.player_22,
        thisgame.player_23,
    }
    if thisuser in player_list:
        return True
    else:
        return False


def is_host(thisuser,thisgame):
    return (thisuser == thisgame.player_11)


def host_queue_update(thisgame):
    #this function updates the host about the players in the queue
    this_group_name = "unite-" + thisgame.unite_id + "-host"
    print('asset ' + this_group_name)
    this_queue = str(list(thisgame.unite_queue.players.all()))
    this_host_queue_update = {
        "type": 'queue_update',
        'time': str(timezone.now()),
        'unite_id': thisgame.unite_id,
        'queue': this_queue,
    }
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        this_group_name, {
            "type": 'queue_update',
            "content": json.dumps(this_host_queue_update),
        })

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




def game_details_generator(thisgame): #returns the game details as json, which is needed only once during the game
    game_details = {'game_name':thisgame.game_name,'game_id':thisgame.game_id,'game_status':thisgame.game_status,
                    'p11':{'id':thisgame.player_11,'img':thisgame.player_11_image,},
                    'p12':{'id':thisgame.player_12,'img':thisgame.player_12_image,},
                    'p13':{'id':thisgame.player_13,'img':thisgame.player_13_image,},
                    'p21':{'id':thisgame.player_21,'img':thisgame.player_21_image,},
                    'p22':{'id':thisgame.player_22,'img':thisgame.player_22_image,},
                    'p23':{'id':thisgame.player_23,'img':thisgame.player_23_image,},
    }
    return game_details

def current_status_generator(thisgame): #returns the game status as json, which is needed for every move in the game
    current_status ={'time': str(timezone.now()),
                    'p11hand':thisgame.player_11_hand,
                    'p12hand':thisgame.player_12_hand,
                    'p13hand':thisgame.player_13_hand,
                    'p21hand':thisgame.player_23_hand,
                    'p22hand':thisgame.player_22_hand,
                    'p23hand':thisgame.player_23_hand,
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







#test and trial functions
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
