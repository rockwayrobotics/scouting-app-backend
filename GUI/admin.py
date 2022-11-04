from django.contrib import admin

from .models import MatchResult, Event, Registration, Team

admin.site.register(MatchResult)
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(Registration)
