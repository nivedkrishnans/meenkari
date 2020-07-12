from django.contrib import admin
from .models import *
# Register your models here.

class GameResource(admin.ModelAdmin):
    list_display = ('game_name','game_id','create_time','game_status',)
    list_filter  = ('create_time','game_status',)
    class Meta:
        model = Game


admin.site.register(Game,GameResource)
admin.site.register(UniteQueue)
