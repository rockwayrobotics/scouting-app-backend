from django.http import HttpResponse
from django.views import View
from django.template import loader
from django.shortcuts import render

from .models import MatchResult, Event, Team, Registration

from .blueAllianceAPI import get_data

from .opencv import exe


def index(request):
    template = loader.get_template('scouting_app/index.html')
    return HttpResponse(template.render())


def match_details(request, event_id, this_match_number):
    try:
        this_event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponse("Event not found")  # improve to return actual html

    this_match = MatchResult.objects.filter(linked_event=this_event).filter(match_number=this_match_number).order_by(
        'linked_team__number')  # List of all matches from event that match the number

    context = {
        'latest_match_list': this_match, 'event': this_event, 'match_number': this_match[:1].get().match_number
    }

    return render(request, 'scouting_app/matchDetails.html', context)


def team_details(request, team_number):
    team_data = Team.objects.get(number=team_number)
    context = {'team': team_data}
    return render(request, 'scouting_app/teamDetails.html', context)


def team_at_event(request, event_id, team_number):
    this_event = Event.objects.get(id=event_id)
    this_team = Team.objects.get(number=team_number)

    latest_match_list = MatchResult.objects.filter(linked_event=this_event).filter(linked_team=this_team).order_by(
        'recorded_time')

    context = {'latest_match_list': latest_match_list, 'event_name': "at " + this_event.name, 'team': this_team}
    return render(request, 'scouting_app/teamDetails.html', context)


def team_on_match(request, event_id, team_number, this_match_number):
    this_event = Event.objects.get(id=event_id)
    this_team = Team.objects.get(number=team_number)

    context = {'team': this_team, 'event': this_event, 'match_number': this_match_number}
    return render(request, 'scouting_app/teamMatchDetails.html', context)


def event_details(request, event_id):
    this_event = Event.objects.get(id=event_id)

    latest_match_list = MatchResult.objects.filter(linked_event=this_event).order_by('match_number')

    unique_match_list = latest_match_list.values_list('match_number').distinct()

    attending_teams = Registration.objects.filter(registered_event=this_event).order_by('registered_team__number')

    context = {'latest_match_list': latest_match_list, 'event': this_event, 'attending_teams': attending_teams,
               'unique_match_list': unique_match_list}
    return render(request, 'scouting_app/event.html', context)


def event_list(request):
    latest_event_list = Event.objects.order_by('start_date')

    context = {'latest_event_list': latest_event_list}
    return render(request, 'scouting_app/event_list.html', context)


def team_list(request):
    teams_list = Team.objects.order_by('number')

    context = {'teams': teams_list}
    return render(request, 'scouting_app/team_list.html', context)


def test(request):
    get_data()
    return HttpResponse("OH YEAH")

def vis_test(request):
    exe()
    return HttpResponse("Beans")
