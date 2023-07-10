from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from . import views
from . import game
import django_registration
from django_registration.backends.one_step.views import RegistrationView #not needed if using 2-step registration with email

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('host/', views.host, name="host"),
    path('join/', views.join, name="join"),
    path('sorry/', views.sorry, name="sorry"),
    path('gameover/', views.gameover, name="gameover"),
    path('error/', views.error, name="error"),
    path('lobby/<str:url_id>', views.lobby, name="lobby"),
    path('play/<str:url_id>', views.play, name="play"),
    path('valet/<str:url_id>', game.valet, name="valet"),
    path('game_status/<str:url_id>', views.game_status, name="game_status"),
    
    path('accounts/register/', RegistrationView.as_view(success_url='/'),name='django_registration_register'), #remove this to get 2-step registration with email
    path('accounts/', include('django_registration.backends.one_step.urls')), #remove this to get 2-step registration with email
    
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

]
