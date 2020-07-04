from django.utils import timezone
from .models import *
import string
import random
import json
from asgiref.sync import async_to_sync
import channels.layers
from django.conf import settings


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

delimiter = ","


def shuffle_cards(thisgame): #the argument is a game instance
    shuffleddeck= random.sample(newdeck, k=54)
    thisgame.player_11_hand =  delimiter.join(shuffleddeck[0:9]) + delimiter
    thisgame.player_12_hand =  delimiter.join(shuffleddeck[9:18]) + delimiter
    thisgame.player_13_hand =  delimiter.join(shuffleddeck[18:27]) + delimiter
    thisgame.player_21_hand =  delimiter.join(shuffleddeck[27:36]) + delimiter
    thisgame.player_22_hand =  delimiter.join(shuffleddeck[36:45]) + delimiter
    thisgame.player_23_hand =  delimiter.join(shuffleddeck[45:54]) + delimiter
    thisgame.save();

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



def broadcast_live(current_status):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        settings.LIVE_GROUP_NAME, {
            "type": 'game_update',
            "content": json.dumps(current_status),
        })
