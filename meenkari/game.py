from .models import *
from .assets import *
from django.utils import timezone
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User 
from django.views.decorators.csrf import csrf_exempt


#The valet is a view function that has been kept separate from the rest to make things less cluttered
#The game page sends user's actions as an ajax request to the valet
#The valet makes the appropriate actions and updates the six players 
#It also returns an HttpResponse for the ajax

"""
HttpResponse values for the ajax request
0 : bad request
1 : received and okay
2 : invalid game_id
3 : invalid current player
"""

"""
ajax request formats:
{
    'action': <ask/declare/misdeclare>,
    'toplayer': <username of player to whom the card is asked (only for action - ask)>,
    'askcard': <card that is being asked (only for action - ask)>,
    'suit': <half suit that is being misdeclared (only for action - misdeclare)>,
    
}
"""

#The view is exempted from using csrf token. to be fixed.
@csrf_exempt
def valet(request, url_id=1):
    print("request recieved " , request.method)
    this_game = Game.objects.get(game_id=url_id)
    this_game.log = this_game.log + '\n' + str(timezone.now())
    #recieves the json from the request. the json is available as a dict key for some reason
    #please find a neater way to do this :'-)
    request_json = (list((request.POST.dict().keys())))[0]
    request_json = json.loads(json.dumps(request_json))
    print(request_json)
    #checking whether user is logged in
    if request.user.is_authenticated:
        #saving the user into a variable
        this_user = request.user
        #checking if the game_id is valid
        try:
            this_game = Game.objects.get(game_id=url_id)
        except:
            print('Invalid game_id')
            return HttpResponse(2)
        
        #checks if the request is from the current player otherwise returns 'invalid current player'
        if is_current_player(this_user,this_game):
            print('Current Player Validated: ',this_user)

            #Actual processing of the move
            request_json = { 'toplayer': "adit123456", 'suit': "1", 'askcard': "11", 'action': "Ask" }
            return meenkari(request_json, this_user, this_game)

        else:
            print('Current Player Invalid: ',this_user)
            return HttpResponse(3)

        

    else:       
        #if the user is not logged in, a 0 is sent back, meaning 'bad response'
        print('User not logged in')
        return HttpResponse(0)
    

def meenkari(request_json, this_user, this_game):
    #After doin the basic checks like whether the player is valid, etc, the valet()
    #asks meenkari() to perform the right actions according to contents of the json
    print('meenkari initiated')
    action  = request_json['action']
    team1 = [str(this_game.p1),str(this_game.p3),str(this_game.p5)]
    team2 = [str(this_game.p2),str(this_game.p4),str(this_game.p6)]

    if action == 'ask':
        if (this_user in team1 and request_json['toplayer'] in team2) or (this_user in team2 and request_json['toplayer'] in team1):
            card = request_json["askcard"]
            if has_suit(suit, this_user, this_game):
                print("Valid suit")
                if has_card(card,request_json["toplayer"],this_game):
                    print("Card recieved")
                    remove_card(card,toplayer,this_game)
                    add_card(card, this_user, this_game)                    
                    log = '\n' + str(timezone.now()) + ' - ' + ' ' + this_user + ' received ' + card + ' from ' + request_json["toplayer"]
                    this_game.log = this_game.log + log
                    this_game.save()
                    print(log)
                else:
                    this_game.p0 = request_json["toplayer"]
                    log = '\n' + str(timezone.now()) + ' - ' + ' ' + this_user + ' asked for ' + card + ' to ' + request_json["toplayer"] + ' but didnt recieve it'
                    this_game.log = this_game.log + log
                    this_game.save()
                    print(log)
            else:
                return 0
        else:
            return 0


    game_status_broadcast(this_game)
    return 1


def remove_card(card,this_player,this_game):
    this_player = str(this_player)
    card = card + ','

    if this_game.p1 == this_player:
        temp = this_game.p1_hand
        this_game.p1_hand = (this_game.p1_hand).replace(card,'')
        this_game.save()
        return card in temp
    elif this_game.p2 == this_player:
        temp = this_game.p2_hand
        this_game.p2_hand = (this_game.p2_hand).replace(card,'')
        this_game.save()
        return card in temp
    elif this_game.p3 == this_player:
        temp = this_game.p3_hand
        this_game.p3_hand = (this_game.p3_hand).replace(card,'')
        this_game.save()
        return card in temp
    elif this_game.p4 == this_player:
        temp = this_game.p4_hand
        this_game.p4_hand = (this_game.p4_hand).replace(card,'')
        this_game.save()
        return card in temp
    elif this_game.p5 == this_player:
        temp = this_game.p5_hand
        this_game.p5_hand = (this_game.p5_hand).replace(card,'')
        this_game.save()
        return card in temp
    elif this_game.p6 == this_player:
        temp = this_game.p6_hand
        this_game.p6_hand = (this_game.p6_hand).replace(card,'')
        this_game.save()
        return card in temp
    else:
        return False
    
def delete_card(card,this_game):
    #removes the card from all players in the game
    card = card + ','
    this_game.p1_hand = (this_game.p3_hand).replace(card,'')
    this_game.p2_hand = (this_game.p3_hand).replace(card,'')
    this_game.p3_hand = (this_game.p3_hand).replace(card,'')
    this_game.p4_hand = (this_game.p3_hand).replace(card,'')
    this_game.p5_hand = (this_game.p3_hand).replace(card,'')
    this_game.p6_hand = (this_game.p3_hand).replace(card,'')

    this_game.save()

def add_card(card,this_player,this_game):
    this_player = str(this_player)
    card = card + ','

    if this_game.p1 == this_player:
        if card not in this_game.p1_hand:
            this_game.p1_hand = (this_game.p1_hand) + card
            this_game.save()
            return True
    elif this_game.p2 == this_player:
        if card not in this_game.p2_hand:
            this_game.p2_hand = (this_game.p2_hand) + card
            this_game.save()
            return True
    elif this_game.p3 == this_player:
        if card not in this_game.p3_hand:
            this_game.p3_hand = (this_game.p3_hand) + card
            this_game.save()
            return True
    elif this_game.p4 == this_player:
        if card not in this_game.p1_hand:
            this_game.p4_hand = (this_game.p4_hand) + card
            this_game.save()
            return True
    elif this_game.p5 == this_player:
        if card not in this_game.p5_hand:
            this_game.p5_hand = (this_game.p5_hand) + card
            this_game.save()
            return True
    elif this_game.p6 == this_player:
        if card not in this_game.p6_hand:
            this_game.p6_hand = (this_game.p6_hand) + card
            this_game.save()
            return True
    
    return False
    
def has_suit(suit, this_user, this_game):
    temp = ''
    if this_game.p1 == this_player:
        temp = this_game.p1_hand
    elif this_game.p2 == this_player:
        temp = this_game.p2_hand
    elif this_game.p3 == this_player:
        temp = this_game.p3_hand
    elif this_game.p4 == this_player:
        temp = this_game.p4_hand
    elif this_game.p5 == this_player:
        temp = this_game.p5_hand
    elif this_game.p6 == this_player:
        temp = this_game.p6_hand

    cards = temp.split()
    for i in cards:
        if i.startswith(suit):
            return True
    return False

def has_card(card, this_user, this_game):
    temp = ''
    if this_game.p1 == this_player:
        temp = this_game.p1_hand
    elif this_game.p2 == this_player:
        temp = this_game.p2_hand
    elif this_game.p3 == this_player:
        temp = this_game.p3_hand
    elif this_game.p4 == this_player:
        temp = this_game.p4_hand
    elif this_game.p5 == this_player:
        temp = this_game.p5_hand
    elif this_game.p6 == this_player:
        temp = this_game.p6_hand

    cards = temp.split()
    for i in cards:
        if i.startswith(card):
            return True
    return False
