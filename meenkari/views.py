from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .assets import *
import string
import random
from django.utils import timezone
from django.contrib import messages
import json
from django.http import HttpResponse, JsonResponse
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
                newLobby = Lobby(game=newgame)
                newLobby.save()
                messages.add_message(request, messages.INFO, 'You have succesfully hosted the game ' + (newgame.game_name) + '. You can lobby with your teammembers at lobby/' + (newgame.lobby_id))
                return redirect('lobby', url_id=(newgame.lobby_id))
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
        game_list = list(Game.objects.filter(Q(game_privacy='public') & ~Q(game_status='over') & ~Q(game_status='stopped') ).order_by('-create_time'))[:10]
        #game_list = list(Game.objects.all().order_by('-create_time'))
        return render(request, 'meenkari/join.html',{'game_list':game_list})
    else:
        messages.add_message(request, messages.INFO, 'Please log in in order to join games')
        return redirect('login')

def lobby(request,url_id=1):
    if request.user.is_authenticated:
        this_game = get_object_or_404(Game, lobby_id=url_id)
        this_user = request.user
        if this_game.game_status == 'empty':
            if is_host(this_user,this_game):
                if request.method == "POST":
                    print("POOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOST")
                    f = HostLobbyForm(request.POST)
                    if f.is_valid():
                        this_game.p2 = User.objects.get(username=f.cleaned_data['p2'])
                        this_game.p3 = User.objects.get(username=f.cleaned_data['p3'])
                        this_game.p4 = User.objects.get(username=f.cleaned_data['p4'])
                        this_game.p5 = User.objects.get(username=f.cleaned_data['p5'])
                        this_game.p6 = User.objects.get(username=f.cleaned_data['p6'])
                        this_game.game_status = "united"
                        this_game.lastmodify_time = timezone.now()
                        random_p0(this_game)
                        this_game.save()
                        messages.add_message(request, messages.INFO, 'You have succesfully started the game ' + (this_game.game_name) + '. You can play with your teammembers at play/' + (this_game.game_id))
                        player_lobby_update(this_game)
                        return redirect('play', url_id=(this_game.game_id))
                    else:
                        return render(request, 'meenkari/lobby_host.html', {'form': f,'lobby':lobby_json(this_game)})
                else:
                    f = HostLobbyForm(initial={'p1':this_game.p1.username,})
                    #f = HostLobbyForm(initial={'p1':this_game.p1.username,'p2':this_game.p2.username,'p3':this_game.p3.username,'p4':this_game.p4.username,'p5':this_game.p5.username,'p6':this_game.p6.username})
                    return render(request, 'meenkari/lobby_host.html', {'form': f,'lobby':lobby_json(this_game)})

            else:
                this_game.lobby.players.add(this_user)
                host_lobby_update(this_game)
                return render(request, 'meenkari/lobby_player.html',)
        else:
            if is_player(this_user,this_game):
                if this_game.game_status in ['over','stopped']:
                    return render(request, 'meenkari/gameover.html',)
                elif this_game.game_status in ['united','started']:
                    return redirect('play', url_id=(this_game.game_id))
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
                game_status = game_status_json(this_user,this_game,log_generate(this_game))
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

from django.views.decorators.csrf import csrf_exempt
#The view is exempted from using csrf token. to be fixed.
@csrf_exempt
def game_status(request,url_id=1):
    if request.user.is_authenticated:
        this_user = request.user
        try:
            this_game = Game.objects.get(game_id=url_id)
        except:
            return HttpResponse(0)
        
        data = game_status_json(this_user, this_game, log_generate(this_game))
        return JsonResponse(data, safe=False)
    
    return HttpResponse(0)


