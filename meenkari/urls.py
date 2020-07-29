from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from . import views
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
    path('unite/<str:url_id>', views.unite, name="unite"),
    path('play/<str:url_id>', views.play, name="play"),
    
    path('accounts/register/', RegistrationView.as_view(success_url='/'),name='django_registration_register'), #remove this to get 2-step registration with email
    path('accounts/', include('django_registration.backends.one_step.urls')), #remove this to get 2-step registration with email
    
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #trial and test pages below

    path('start/', views.start, name="start"),
    path('game/<str:url_id>', views.game, name="game"),
    path('communication_test', views.communication_test, name="communication_test"),
    path('communication_test2', views.communication_test2, name="communication_test2"),
    path('communication_test2_trigger', views.communication_test2_trigger, name="communication_test2_trigger"),
]
