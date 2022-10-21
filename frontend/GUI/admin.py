from django.contrib import admin

from .models import matchResult, event, team

admin.site.register(matchResult)
admin.site.register(event)
admin.site.register(team)
