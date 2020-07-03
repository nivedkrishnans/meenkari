from django.shortcuts import render
from .forms import *
from .models import *
from .assets import *
import string
import random
from django.utils import timezone
from django.contrib import messages
import json
from django.http import HttpResponse

game_id_size = 32

# Create your views here.
def start(request):
    if request.method == "POST":
        f = StartGameForm(request.POST)
        if f.is_valid():
            newgame = f.save(commit=False)
            random_id_chosen = False
            all_games_id = Game.objects.all().values('game_id')
            while not random_id_chosen:
              random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k = game_id_size))
              if (random_id not in all_games_id):
                random_id_chosen = True
                newgame.game_id = random_id
            shuffle_cards(newgame)
            newgame.game_status = "open"
            newgame.create_time = timezone.now()
            newgame.save()
            messages.add_message(request, messages.INFO, 'You have succesfully started the game ' + (newgame.game_name) + ' at ' + (newgame.game_id))
            return render(request, 'fishmarket/start.html', {'form': f})
    else:
        f = StartGameForm()
    return render(request, 'fishmarket/start.html', {'form': f})

def game(request):
    this_game = Game.objects.order_by('-create_time')[0] #until i figure out how to do the selection based on game_id right
    #this_game = get_object_or_404(Game, game_id=url_id)
    this_game_details = json.dumps(game_details_generator(this_game))
    this_game_status = json.dumps(game_status_generator(this_game))
    return render(request, 'fishmarket/game.html',{'game_details':this_game_details,'game_status':this_game_status})


def communication_test(request):
    this_game = Game.objects.order_by('-create_time')[0] #until i figure out how to do the selection based on game_id right
    p11_hand = this_game.player_11_hand
    return render(request, 'fishmarket/communication_test.html',{'p11_hand':p11_hand})
