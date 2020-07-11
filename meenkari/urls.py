from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from . import views
import django_registration

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('host/', views.host, name="host"),
    path('join/', views.join, name="join"),
    path('sorry/', views.sorry, name="sorry"),
    path('unite/<str:url_id>', views.unite, name="unite"),
    path('play/<str:url_id>', views.play, name="play"),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #trial and test pages below

    path('start/', views.start, name="start"),
    path('game/<str:url_id>', views.game, name="game"),
    path('communication_test', views.communication_test, name="communication_test"),
    path('communication_test2', views.communication_test2, name="communication_test2"),
    path('communication_test2_trigger', views.communication_test2_trigger, name="communication_test2_trigger"),
]
