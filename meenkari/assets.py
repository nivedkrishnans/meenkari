from django.utils import timezone
from datetime import datetime
from .models import *
import string
import random
import json
from asgiref.sync import async_to_sync
import channels.layers
from django.conf import settings


# IMPORTANT: For all jsons to be sent to the client, use double quotes inside and single quotes at the very outside


delimiter = ","
game_id_size = 32
lobby_id_size = 32


def random_string_generator(size):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=size))


newdeck = [str(i)+str(j) for i in range(1,10) for j in range(1,7)] # the 9 half-suits and their 6 cards (Named 11-16, 21-26,...91-96)


# the argument is a game instance
def shuffle_cards(thisgame):
    # the function first randomly arranges the cards, splits it into hands of 9 cards each, and then sorts the individual hands before giving it to the players
    shuffleddeck = random.sample(newdeck, k=54)
    for i in range(1,7):
        # Using  locals() to refer to a variable via its name as a string. Eg: locals()['t1'] = 3 is same as t1=3
        var_name = "t"+str(i) # t1, t2, etc as temporary variables
        locals()[var_name] = shuffleddeck[(i-1)*9:i*9]
        locals()[var_name].sort() 
        model_attribute = "p"+str(i)+"_hand" # p1_hand, p2_hand, etc from game model
        player_hand = delimiter.join(locals()[var_name]) + delimiter # Each card is two digits with a comma after. Eg for player hand: "12,32,54,91,"
        setattr(thisgame, model_attribute, player_hand) 
    thisgame.save()
    print("Cards shuffled")


def display_hands(thisgame):
    hands = [ getattr(thisgame, "p"+str(i)+"_hand") for i in range(1,7)]
    # print(hands)


def assign_id(thisgame):
    # this function assigns random strings as game_id and lobby_id for the game instance passed as argument.
    # the length of the random strings is defined by game_id_size and lobby_id_size declared globally
    all_game_ids = Game.objects.all().values('game_id')
    all_lobby_ids = Game.objects.all().values('lobby_id')

    # choosing game_id
    random_id_chosen = False
    while not random_id_chosen:
        random_id = random_string_generator(
            game_id_size)
        if (random_id not in all_game_ids):
            random_id_chosen = True
            thisgame.game_id = random_id

    # choosing lobby_id
    random_id_chosen = False
    while not random_id_chosen:
        random_id = random_string_generator(
            lobby_id_size)
        if (random_id not in all_lobby_ids):
            random_id_chosen = True
            thisgame.lobby_id = random_id

    thisgame.save()


def is_player(thisuser, thisgame):
    player_list = [str(getattr(thisgame, "p"+str(i)) )for i in range(1,7)]
    if str(thisuser) in player_list:
        return True
    else:
        return False


def is_host(thisuser, thisgame):
    return (thisuser == thisgame.p1)


def is_current_player(thisuser, thisgame):
    return (thisuser == thisgame.p0)


def host_lobby_update(thisgame):
    # this function updates the host about the players in the queue
    this_group_name = "lobby-" + thisgame.lobby_id + "-host"
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        this_group_name, {
            "type": 'lobby_update',
            "content": json.dumps(lobby_json(thisgame)),
        })


def lobby_json(thisgame):
    # this function generates the present player queue inorder to show the host
    this_queue = list(thisgame.lobby.players.all(
    ).values_list("username", flat=True))
    this_queue_json = {
        "type": "lobby_update",
        "time": str(timezone.now()),
        "lobby_id": thisgame.lobby_id,
        "queue": this_queue,
    }
    return this_queue_json


def player_lobby_update(thisgame):
    # this function updates the non-host that the players have been chosen. they players will be asked to reload the page
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


def game_status_json(thisuser, thisgame, message):
    # arguments are a user instance and a game instance, and a string/integer which carries some message to the client
    hand_lengths = [ int(len(getattr(thisgame, "p"+str(i)+"_hand"))/3) for i in range(1,7)]

    game_status_json = {
        "ty": "gsj",
        "ts": datetime.timestamp(timezone.now()),
        "hl": hand_lengths,
        "my": player_status_finder(thisuser, thisgame),
        "te": [thisgame.team_1_status, thisgame.team_2_status],
        "p0": str(thisgame.p0),
        "me": message,
    }
    return json.dumps(game_status_json)


def game_info_json(thisgame):
    game_info = {
        "pl": [str(thisgame.p1), str(thisgame.p2), str(thisgame.p3), str(thisgame.p4), str(thisgame.p5), str(thisgame.p6), ],
        "na": thisgame.game_name,
        "pr": thisgame.game_privacy,
        "ts": str(thisgame.create_time),
    }
    return json.dumps(game_info)


def player_status_finder(thisuser, thisgame):
    # finds the number (1-6) and the hand of a user in a game
    for i in range(1,7):
        if str(thisuser) == str(getattr(thisgame,'p'+str(i))):
            return [i, getattr(thisgame,'p'+str(i)+'_hand')]
    # zero means the player isn't a part of the game
    return [0, "error"]


def game_status_update(thisuser, thisgame, message):
    # this function sends the game_status_json to the players on the game page in an active game
    this_group_name = game_group_name(thisuser, thisgame.game_id)
    channel_layer = channels.layers.get_channel_layer()
    print("Sending game update to ", str(thisuser), "for", this_group_name)
    async_to_sync(channel_layer.group_send)(
        this_group_name, {
            "type": 'game_update',
            "content": json.dumps(game_status_json(thisuser, thisgame, message)),
        })


def game_status_broadcast(thisgame):
    # broadcasts the game status to all 6 players
    try:
        players = [getattr(thisgame, "p"+str(i)) for i in range(1,7)]
    except Exception as e:
        print(e)

    message = log_generate(thisgame)
    print('Recent game history (logs) generated')
    print('Initiating game_status_update for the players')
    for player in players:
        game_status_update(player, thisgame, message)


def log_generate(thisgame):
    all_log_lines = (thisgame.log).splitlines()
    log_length = len(all_log_lines)
    if log_length >= 3:
        log = all_log_lines[log_length -
                            3:log_length]
    elif log_length > 0:
        log = all_log_lines[0:log_length]
    else:
        log = ['Game created']
    log = "<p>" + "</p><p>".join(log) + "</p>"
    return log


def random_p0(thisgame):
    # this function assigns the first player randomly
    players = [getattr(thisgame, "p"+str(i)) for i in range(1,7)]
    thisgame.p0 = players[random.randint(0, 5)]
    thisgame.save()
    print('Assigned first player: ', thisgame.p0, thisgame)


def tester_sender(group, message):
    # this function sends the message from the tester to the given group
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {
            "type": 'game_update',
            "content": json.dumps(message),
        })


suitlist = {
    "1": "8 and J",
    "2": "High ♠",
    "3": "High ◆",
    "4": "High ♣",
    "5": "High ♥",
    "6": "Low ♠",
    "7": "Low ◆",
    "8": "Low ♣",
    "9": "Low ♥"
}


def makecardlist():
    cardlist = {
        "11": "Black J",
        "12": "8 of ♠",
        "13": "8 of ◆",
        "14": "8 of ♣",
        "15": "8 of ♥",
        "16": "White J",
    }

    lower = ["2", "3", "4", "5", "6", "7"]
    higher = ["9", "10", "Jack", "Queen", "King", "Ace"]
    suit = ["♠", "◆", "♣", "♥"]

    for i in range(4):
        for j in range(6):
            cardlist[str(i+2)+str(j+1)] = higher[j]+" of "+suit[i]

    for i in range(4):
        for j in range(6):
            cardlist[str(i+6)+str(j+1)] = lower[j]+" of "+suit[i]

    return cardlist


cardlist = makecardlist()



def lobby_group_name(user, url_id):
    # Create the name for the channels group for the LobbyConsumer
    this_game = Game.objects.get(lobby_id=url_id)
    if is_host(user,this_game):
        this_user_group = "lobby-" + url_id + "-host"
    else:
        this_user_group = "lobby-" + url_id + "-queue"
    return this_user_group

def game_group_name(user, url_id):
    # Create the name for the channels group for the GameConsumer
    this_game = Game.objects.get(game_id=url_id)
    if is_player(user, this_game):
        this_user_group = "game-" + this_game.game_id + "-" + str(user)
    else:
        this_user_group = "denied"
    return this_user_group