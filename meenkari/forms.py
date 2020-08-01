from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.utils.translation import gettext_lazy as _

class TesterForm(forms.Form):
    group = forms.CharField(label="Group", max_length=1000, widget=forms.TextInput(),)
    message = forms.CharField(label="Message", max_length=1000, widget=forms.TextInput(),)
    
    
class HostForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('game_name','game_privacy')
        labels = {
            'game_name':'Game Name',
            'game_privacy':'Do you want the game to appear on the join page?',
        }



class HostLobbyForm(forms.Form):
    #p1 value has to be passed directly into it from the view inorder to do the rest of the validation
    #specifically making p1 readonly
    p1 = forms.CharField(label="Team 1 Player 1", max_length=32, widget=forms.TextInput(attrs={'readonly':True}))
    #p1 = forms.CharField(label="Team 1 Player 1", max_length=32, readonly=True)
    p2 = forms.CharField(label="Team 1 Player 2", max_length=32,)
    p3 = forms.CharField(label="Team 1 Player 3", max_length=32,)
    p4 = forms.CharField(label="Team 2 Player 1", max_length=32,)
    p5 = forms.CharField(label="Team 2 Player 2", max_length=32,)
    p6 = forms.CharField(label="Team 2 Player 3", max_length=32,)

    #custom Validation . see https://www.geeksforgeeks.org/python-form-validation-using-django/
    def clean_p1(self):
        super(HostLobbyForm, self).clean()
        p1 = self.cleaned_data['p1']
        users = User.objects.filter(username=p1)
        if not users:
            raise  ValidationError(_("Invalid user"))
        return p1
    def clean_p2(self):
        super(HostLobbyForm, self).clean()
        p2 = self.cleaned_data['p2']
        users = User.objects.filter(username=p2)
        if not users:
            raise  ValidationError(_("Invalid user"))
        return p2
    def clean_p3(self):
        super(HostLobbyForm, self).clean()
        p3 = self.cleaned_data['p3']
        users = User.objects.filter(username=p3)
        if not users:
            raise  ValidationError(_("Invalid user"))
        return p3
    def clean_p4(self):
        super(HostLobbyForm, self).clean()
        p4 = self.cleaned_data['p4']
        users = User.objects.filter(username=p4)
        if not users:
            raise  ValidationError(_("Invalid user"))
        return p4
    def clean_p5(self):
        super(HostLobbyForm, self).clean()
        p5 = self.cleaned_data['p5']
        users = User.objects.filter(username=p5)
        if not users:
            raise  ValidationError(_("Invalid user"))
        return p5
    def clean_p6(self):
        super(HostLobbyForm, self).clean()
        p6 = self.cleaned_data['p6']
        users = User.objects.filter(username=p6)
        if not users:
            raise  ValidationError(_("Invalid user"))
        return p6

    def clean(self):
        p1 = self.cleaned_data.get('p1')
        p2 = self.cleaned_data.get('p2')
        p3 = self.cleaned_data.get('p3')
        p4 = self.cleaned_data.get('p4')
        p5 = self.cleaned_data.get('p5')
        p6 = self.cleaned_data.get('p6')
        temp = [p1,p2,p3,p4,p5,p6]
        if not (len(temp) == len(set(temp))):
            raise  ValidationError(_("Same user appears in multiple positions"))

#        all_users = User.objects.all().values('username')
#        temp = []
#        if not p1 in all_users:
#            self._errors['p1'] = self.error_class(['Invalid user or user already selected'])
#        temp.append(p1)
#        if (not p2 in all_users) or (p2 in temp):
#            self._errors['p2'] = self.error_class(['Invalid user or user already selected'])
#        temp.append(p2)
#        if (not p3 in all_users) or (p3 in temp):
#            self._errors['p3'] = self.error_class(['Invalid user or user already selected'])
#        temp.append(p3)
#        if (not p4 in all_users) or (p4 in temp):
#            self._errors['p4'] = self.error_class(['Invalid user or user already selected'])
#        temp.append(p4)
#        if (not p5 in all_users) or (p5 in temp):
#            self._errors['p5'] = self.error_class(['Invalid user or user already selected'])
#        temp.append(p5)
#        if (not p6 in all_users) or (p6 in temp):
#            self._errors['p6'] = self.error_class(['Invalid user or user already selected'])
#
#        # return any errors if found
#        return self.cleaned_data




#below are test and trial forms.


#class HostLobbyFormOld(forms.ModelForm):
#    class Meta:
#        model = Game
#        fields = ('p1','p2','p3','p4','p5','p6',)
#        widgets = {
#            'p1' : forms.TextInput(attrs={'readonly':True}),
#            'p2' : forms.TextInput(),
#            'p3' : forms.TextInput(),
#            'p4' : forms.TextInput(),
#            'p5' : forms.TextInput(),
#            'p6' : forms.TextInput(),
#        }
#        def clean_p1(self):
#            return
#        #custom validation to check if the same user appears multiple times
#        def clean(self):
#            p1 = self.cleaned_data.get('p1')
#            p2 = self.cleaned_data.get('p2')
#            p3 = self.cleaned_data.get('p3')
#            p4 = self.cleaned_data.get('p4')
#            p5 = self.cleaned_data.get('p5')
#            p6 = self.cleaned_data.get('p6')
#            temp = [p1,p2,p3,p4,p5,p6]
#            if not (len(temp) == len(set(temp))):
#                raise  ValidationError(_("Same user appears in multiple positions"))
#


#class StartGameForm(forms.ModelForm):
#    class Meta:
#        model = Game
#        fields = ('game_name','player_11', 'player_11_image','p2','p2_image','p3','p3_image','p4','p4_image','p5','p5_image','p6','p6_image')
