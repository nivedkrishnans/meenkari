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
4 : player has no cards
5 : halfsuit already declared
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
    #recieves the json from the request. the json is available as a dict key for some reason
    #please find a neater way to do this :'-)
    # request_json_temp = (list((request.POST.dict().keys())))[0]
    request_json_temp = request.POST.get('json')
    print(type(request_json_temp), request_json_temp)
    request_json = json.loads(str(request_json_temp))
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
        
        

        #Actual processing of the move
        meenkari_result =  meenkari(request_json, this_user, this_game)
        game_status_broadcast(this_game) #broadcasts the changes before returning the meenkari result, as the return statement stops the function
        return meenkari_result


        

    else:       
        #if the user is not logged in, a 0 is sent back, meaning 'bad response'
        print('User not logged in')
        return HttpResponse(0)
    

def meenkari(request_json, this_user, this_game):
    #After doin the basic checks like whether the player is valid, etc, the valet()
    #asks meenkari() to perform the right actions according to contents of the json
    print('meenkari initiated')
    try:
        action = request_json['action']
        print('Action: ',action)
    except Exception as e:
        print(e)
    print("Actions in request: ",action)
    team1 = [str(this_game.p1),str(this_game.p3),str(this_game.p5)]
    team2 = [str(this_game.p2),str(this_game.p4),str(this_game.p6)]
    
    
    if action == 'ask':
        #checks if the request is from the current player otherwise returns 'invalid current player'
        if is_current_player(this_user,this_game):
            this_user = str(this_user)
            print('Current Player Validated: ',this_user)
            print("ask initiated")
            if card_count(request_json['toplayer'],this_game) == 0:
                #if the otehr player does not have cards, the ask is invalid
                return HttpResponse(4)
            if (this_user in team1 and request_json['toplayer'] in team2) or (this_user in team2 and request_json['toplayer'] in team1):
                print('Players are in opposite teams')
                card = request_json["askcard"]
                if has_suit(request_json['suit'], this_user, this_game):
                    if has_card(card,request_json["toplayer"],this_game):
                        print("The other player has the card")
                        remove_card(card,request_json["toplayer"],this_game)
                        add_card(card, this_user, this_game)                    
                        log = '\n' + str(timezone.now().ctime()) + ' - ' + ' ' + this_user + ' received ' + cardlist[card] + ' from ' + request_json["toplayer"]
                        this_game.log = this_game.log + log
                        this_game.save()
                        print(log)
                        return HttpResponse(1)
                    else:
                        try:
                            new_current = User.objects.get(username=request_json["toplayer"])
                            this_game.p0 = new_current
                        except Exception as e:
                            print(e)
                        log = '\n' + str(timezone.now().ctime()) + ' - ' + ' ' + this_user + ' asked for ' + cardlist[card] + ' to ' + request_json["toplayer"] + ' but didnt recieve it'
                        this_game.log = this_game.log + log
                        this_game.save()
                        print(log)
                        return HttpResponse(1)
                else:
                    return HttpResponse(0)
            else:
                return HttpResponse(0)
        else:
            return HttpResponse(3)
    
    elif action == 'declare':
        #card_checker = [] #can be used if we want to know which cards were right and which were wrong
        this_user = str(this_user)
        if suitlist[request_json['suit']] in this_game.team_1_status or suitlist[request_json['suit']] in this_game.team_2_status:
            return HttpResponse(5)
        declare_result = True
        for i in range(1,7):
            card = request_json['suit'] + str(i)
            print('card ', card)
            has_the_card = has_card(card,request_json['card'+str(i)],this_game)
            #card_checker.append(has_the_card)
            declare_result = declare_result and has_the_card #if one card is wrong, the whole thing becomes false
            if not declare_result:
                break
        print('cards checked for suit', request_json['suit'], ' ',  declare_result)

        # success_team stores whether the players team got the point
        success_team = False
        #own_team stores whether the player declared it for their own team or the other team. 
        own_team = (this_user in team1 and request_json['for team'] == 'team1') or (this_user in team2 and request_json['for team'] == 'team2')
        if own_team:
            print('Declaring for own team')
            #that is, if the user is declaring for his own team
            if declare_result:
                log = '\n' + str(timezone.now().ctime()) + ' - ' + ' ' + this_user + ' declared the suit ' + suitlist[request_json['suit']] + ' for team ' + request_json["for team"] + ' successfully. Team ' +  request_json["for team"] + ' gains 1 point.'
                this_game.log = this_game.log + log
                success_team = True
                this_game.save()
                print(log)
            else:
                log = '\n' + str(timezone.now().ctime()) + ' - ' + ' ' + this_user + ' wrongly declared the suit ' + suitlist[request_json['suit']] + ' for team ' + request_json["for team"] + '. Other team gets the point.'
                this_game.log = this_game.log + log
                success_team = False
                this_game.save()
                print(log)
        else:
            print('Declaring for the other team')
            correct = ' correctly ' if declare_result else ' wrongly '
            log = '\n' + str(timezone.now().ctime()) + ' - ' + ' ' + this_user + ' misdeclared the suit ' + suitlist[request_json['suit']] + correct + ' for team ' + request_json["for team"] + '. Other team gets the point.'
            this_game.log = this_game.log + log
            success_team = False
            this_game.save()
            print(log)
        
        remove_suit(request_json['suit'],this_game)
        if (this_user in team1 and success_team) or (this_user in team2 and not success_team) :
            this_game.team_1_status = this_game.team_1_status + suitlist[request_json['suit']] + '<br>'
            this_game.save()
        else:
            this_game.team_2_status = this_game.team_2_status + suitlist[request_json['suit']] + '<br>'
            this_game.save()
        if card_count(this_game.p0, this_game) == 0:
            my_team = team1 if str(this_game.p0) in team1 else team2
            
            for i in my_team:
                if card_count(i, this_game) == 0:
                    my_team.remove(i)
            if len(my_team)>0:
                new_current = random.choice(my_team)
                try:
                    this_game.p0 = User.objects.get(username=new_current)
                    this_game.save()
                except Exception as e:
                    print(e)
        return HttpResponse(1)
            
    
    return HttpResponse(0)

def card_count(this_user,this_game):
    player_attribute_names = ["p"+str(i) for i in range(1,7)] # p1, p2, etc in the game model
    try:
        current_player_position = [p for p in player_attribute_names if str(getattr(this_game, p)) == str(this_user)][0] # Eg is player is game.p4, returns "p4"
    except Exception as e:
        print("Error finding card count:", e)

    count = int(len(getattr(this_game, current_player_position+"_hand"))/3) # Because if current_player_position is p3, then hand will be p3_hand and each card is teo digits followed by a comma
    print('Card count of ', this_user, count)
    return count


def remove_suit(suit,this_game):
    for i in range(1,7): # For each card in the suit
        for j in range(1,7): # For each player in the game
            remove_card(suit+str(i),getattr(this_game, "p"+str(j)),this_game)
    print("Removed suit ", suit)

def remove_card(card,this_user,this_game):
    # Removes a card from a given player in the game
    # Returns true if succesfull
    card = (card + ',') if ',' not in card else card

    for i in range(1,7):
        player_attribute_name = "p"+str(i)
        hand_attribute_name = "p"+str(i)+"_hand"
        if str(this_user) == str(getattr(this_game, player_attribute_name)):
            hand = getattr(this_game, hand_attribute_name)
            setattr(this_game, hand_attribute_name, hand.replace(card,'') )  
            this_game.save()
            return card in hand
    return False
    
def delete_card(card,this_game):
    #removes the card from all players in the game
    card = (card + ',') if ',' not in card else card

    for i in range(1,7):
        hand_attribute_name = "p"+str(i)+"_hand"
        hand = getattr(this_game, hand_attribute_name)
        setattr(this_game, hand_attribute_name, hand.replace(card,'') )  
    this_game.save()

def add_card(card,this_user,this_game):
    # Returns true if succesfull, else false
    card = (card + ',') if ',' not in card else card

    for i in range(1,7):
        player_attribute_name = "p"+str(i)
        hand_attribute_name = "p"+str(i)+"_hand"
        if str(this_user) == str(getattr(this_game, player_attribute_name)):
            hand = getattr(this_game, hand_attribute_name)
            if card not in hand:
                setattr(this_game, hand_attribute_name, hand + card )  
                this_game.save()
                return True
            
    return False
    
def has_suit(suit, this_user, this_game):
    for i in range(1,7):
        player_attribute_name = "p"+str(i)
        hand_attribute_name = "p"+str(i)+"_hand"
        if str(this_user) == str(getattr(this_game, player_attribute_name)):
            hand = getattr(this_game, hand_attribute_name)
            cards = hand.split(',')
            for card in cards:
                if card.startswith(suit):
                    print(this_user, " has the suit")
                    return True
    return False

def has_card(card, this_user, this_game):
    for i in range(1,7):
        player_attribute_name = "p"+str(i)
        hand_attribute_name = "p"+str(i)+"_hand"
        if str(this_user) == str(getattr(this_game, player_attribute_name)):
            hand = getattr(this_game, hand_attribute_name)
            if (card in hand):
                print(this_user, " has the card")
                return True
    return False
