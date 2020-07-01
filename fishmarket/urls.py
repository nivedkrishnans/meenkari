from django.urls import path
from . import views
from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    #url(r'^$', views.start, name="start"),
    url(r'^start/$', views.start, name="start"),
    url(r'^game$', views.g, name="game"),
]
