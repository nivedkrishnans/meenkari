from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('^start/', views.start, name="start"),
    path('game/<str:url_id>', views.game, name="game"),
    path('communication_test', views.communication_test, name="communication_test"),
    path('communication_test2', views.communication_test2, name="communication_test2"),
    path('communication_test2_trigger', views.communication_test2_trigger, name="communication_test2_trigger"),
]
