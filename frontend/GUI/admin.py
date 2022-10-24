from django.contrib import admin

from .models import matchResult, event, registration, team

admin.site.register(matchResult)
admin.site.register(event)
admin.site.register(team)
admin.site.register(registration)
