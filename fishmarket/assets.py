
from .models import *
import string
import random

newdeck = [
    "la02", "la03", "la04", "la05", "la06", "la07", "joa8", "ha09", "ha10", "ha_j", "ha_q", "ha_k", "ha_a",
    "lc02", "lc03", "lc04", "lc05", "lc06", "lc07", "joc8", "hc09", "hc10", "hc_j", "hc_q", "hc_k", "hc_a",
    "lh02", "lh03", "lh04", "lh05", "lh06", "lh07", "joh8", "hh09", "hh10", "hh_j", "hh_q", "hh_k", "hh_a",
    "ld02", "ld03", "ld04", "ld05", "ld06", "ld07", "jod8", "hd09", "hd10", "hd_j", "hd_q", "hd_k", "hd_a",
    "jo_b", "jo_w",
]
delimiter = ","


def shuffle_cards(thisgame): #the argument is a game instance
    shuffleddeck= random.sample(newdeck, k=54)
    thisgame.player_11_hand =  delimiter.join(shuffleddeck[0:9])
    thisgame.player_12_hand =  delimiter.join(shuffleddeck[9:18])
    thisgame.player_13_hand =  delimiter.join(shuffleddeck[18:27])
    thisgame.player_21_hand =  delimiter.join(shuffleddeck[27:36])
    thisgame.player_22_hand =  delimiter.join(shuffleddeck[36:45])
    thisgame.player_23_hand =  delimiter.join(shuffleddeck[45:54])
    thisgame.save();

#alternate function, incomplete
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
    game_details = {'gn':thisgame.game_name,'gi':thisgame.game_id,'gs':thisgame.game_status,
                    'p11':{'id':thisgame.player_11,'im':thisgame.player_11_image,},
                    'p12':{'id':thisgame.player_12,'im':thisgame.player_12_image,},
                    'p13':{'id':thisgame.player_13,'im':thisgame.player_13_image,},
                    'p21':{'id':thisgame.player_21,'im':thisgame.player_21_image,},
                    'p22':{'id':thisgame.player_22,'im':thisgame.player_22_image,},
                    'p23':{'id':thisgame.player_23,'im':thisgame.player_23_image,},
    }
    return game_details

def game_status_generator(thisgame): #returns the game status as json, which is needed for every move in the game
    game_status ={
                    'p11hand':thisgame.player_11_hand,
                    'p12hand':thisgame.player_12_hand,
                    'p13hand':thisgame.player_13_hand,
                    'p21hand':thisgame.player_23_hand,
                    'p22hand':thisgame.player_22_hand,
                    'p23hand':thisgame.player_23_hand,
                    't1':thisgame.team_1_status,
                    't2':thisgame.team_2_status,
                }
    return game_status
