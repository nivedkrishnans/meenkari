from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from . import views

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^start/$', views.start, name="start"),
    url(r'^game$', views.game, name="game"),
    url(r'^communication_test$', views.communication_test, name="communication_test"),
    url(r'^communication_test2$', views.communication_test2, name="communication_test2"),
    url(r'^communication_test2_trigger$', views.communication_test2_trigger, name="communication_test2_trigger"),
]
