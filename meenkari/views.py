from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .assets import *
import string
import random
from django.utils import timezone
from django.contrib import messages
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User

def home(request):
    return render(request, 'meenkari/home.html',)

def host(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            f = HostForm(request.POST)
            if f.is_valid():
                newgame = f.save(commit=False)
                assign_id(newgame)
                shuffle_cards(newgame)
                newgame.p1 = request.user
                newgame.game_status = "empty"
                newgame.lastmodify_time = timezone.now()
                newgame.save()
                newUniteQueue = UniteQueue(game=newgame)
                newUniteQueue.save()
                messages.add_message(request, messages.INFO, 'You have succesfully hosted the game ' + (newgame.game_name) + '. You can unite with your teammembers at unite/' + (newgame.unite_id))
                return render(request, 'meenkari/host.html', {'form': f})
            else:
                return redirect('error')
        else:
            f = HostForm()
        return render(request, 'meenkari/host.html', {'form': f})
    else:
        messages.add_message(request, messages.INFO, 'Please log in in order to host games')
        return redirect('login')


def join(request):
    if request.user.is_authenticated:
        #list all public games that are not over or stopped, latest first
        game_list = list(Game.objects.filter(Q(game_privacy='public') & ~Q(game_status='over') & ~Q(game_status='stopped') ).order_by('-create_time'))
        #game_list = list(Game.objects.all().order_by('-create_time'))
        return render(request, 'meenkari/join.html',{'game_list':game_list})
    else:
        messages.add_message(request, messages.INFO, 'Please log in in order to join games')
        return redirect('login')

def unite(request,url_id=1):
    if request.user.is_authenticated:
        this_game = get_object_or_404(Game, unite_id=url_id)
        this_user = request.user
        if this_game.game_status == 'empty':
            if is_host(this_user,this_game):
                if request.method == "POST":
                    print("POOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOST")
                    f = HostUniteForm(request.POST)
                    if f.is_valid():
                        #new_data = f.save(commit=False)
                        #this_game.p2 = new_data.p2
                        #this_game.p3 = new_data.p3
                        #this_game.p4 = new_data.p4
                        #this_game.p5 = new_data.p5
                        #this_game.p6 = new_data.p6

                        this_game.p2 = User.objects.get(username=f.cleaned_data['p2'])
                        this_game.p3 = User.objects.get(username=f.cleaned_data['p3'])
                        this_game.p4 = User.objects.get(username=f.cleaned_data['p4'])
                        this_game.p5 = User.objects.get(username=f.cleaned_data['p5'])
                        this_game.p6 = User.objects.get(username=f.cleaned_data['p6'])
                        this_game.game_status = "united"
                        this_game.lastmodify_time = timezone.now()
                        this_game.save()
                        messages.add_message(request, messages.INFO, 'You have succesfully started the game ' + (this_game.game_name) + '. You can play with your teammembers at play/' + (this_game.game_id))
                        return render(request, 'meenkari/unite_host.html', {'form': f,'unite_queue':unite_queue_json(this_game)})
                    else:
                        return render(request, 'meenkari/unite_host.html', {'form': f,'unite_queue':unite_queue_json(this_game)})
                else:
                    f = HostUniteForm(initial={'p1':this_game.p1.username})
                    return render(request, 'meenkari/unite_host.html', {'form': f,'unite_queue':unite_queue_json(this_game)})

            else:
                this_game.unite_queue.players.add(this_user)
                host_queue_update(this_game)
                return render(request, 'meenkari/unite_player.html',)
        else:
            if is_player(this_user,this_game):
                if this_game.game_status in ['over','stopped']:
                    return render(request, 'meenkari/gameover.html',)
                elif this_game.game_status in ['united','started']:
                    return redirect('play', url_id=url_id)
                else:
                    return render(request, 'meenkari/error.html',)
            else:
                return render(request, 'meenkari/sorry.html',)
    else:
        messages.add_message(request, messages.INFO, 'Please log in in order to play')
        return redirect('login')

def play(request,url_id=1):
    if request.user.is_authenticated:
        this_user = request.user
        this_game = get_object_or_404(Game, game_id=url_id)
        if is_player(this_user,this_game):
            if this_game.game_status in ['over','stopped']:
                return render(request, 'meenkari/gameover.html',)
            elif this_game.game_status in ['united','started']:
                game_status = game_status_json(this_user,this_game,"0")
                game_info = game_info_json(this_game)
                return render(request, 'meenkari/play.html',{'game_info_json':game_info,"game_status_json":game_status})
            else:
                return render(request, 'meenkari/error.html',)
        else:
            return render(request, 'meenkari/sorry.html',)

    else:
        messages.add_message(request, messages.INFO, 'Please log in in order to play')
        return redirect('login')

def sorry(request):
    return render(request, 'meenkari/sorry.html',)

def gameover(request):
    return render(request, 'meenkari/gameover.html',)

def error(request):
    return render(request, 'meenkari/error.html',)










#test and trail functions below:

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
            return render(request, 'meenkari/start.html', {'form': f})
    else:
        f = StartGameForm()
    return render(request, 'meenkari/start.html', {'form': f})

def game(request,url_id=1):
    #this_game = Game.objects.order_by('-create_time')[0] #until i figure out how to do the selection based on game_id right
    this_game = get_object_or_404(Game, game_id=url_id)
    this_game_details = json.dumps(game_details_generator(this_game))
    this_current_status = json.dumps(current_status_generator(this_game))
    return render(request, 'meenkari/game.html',{'test_id':url_id,'game_details':this_game_details,'current_status':this_current_status})


def communication_test(request):
    this_game = Game.objects.order_by('-create_time')[0] #until i figure out how to do the selection based on game_id right
    p1_hand = this_game.p1_hand
    return render(request, 'meenkari/communication_test.html',{'p1_hand':p1_hand})


def communication_test2(request):
    this_game = Game.objects.order_by('-create_time')[0] #until i figure out how to do the selection based on game_id right
    p1_hand = this_game.p1_hand
    return render(request, 'meenkari/communication_test2.html',{'p1_hand':p1_hand})

def communication_test2_trigger(request):
    this_game = Game.objects.order_by('-create_time')[0] #until i figure out how to do the selection based on game_id right
    this_game_id = "randomegameid"
    this_username = "denied"
    if request.user.is_authenticated:
        this_username = request.user.username
    broadcast_live(current_status_generator(this_game),this_game_id,this_username)
