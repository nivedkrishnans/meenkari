from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.utils.translation import gettext_lazy as _



class HostForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('game_name','game_privacy')
        labels = {
            'game_name':'Game Name',
            'game_privacy':'Do you want the game to appear on the join page?',
        }





#below are test and trial forms.

#class StartGameForm(forms.ModelForm):
#    class Meta:
#        model = Game
#        fields = ('game_name','player_11', 'player_11_image','player_12','player_12_image','player_13','player_13_image','player_21','player_21_image','player_22','player_22_image','player_23','player_23_image')
