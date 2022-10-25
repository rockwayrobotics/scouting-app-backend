from django.http import HttpResponse
from django.views import View
from django.template import loader
from django.shortcuts import render

from .models import TeamData, matchResult, event, team, registration
from .opencv import test_function

from .blueAllianceAPI import getData

def get(self, request, team=0):
    if team:
        try:
            team_data = TeamData.objects.get(id=team)
        except TeamData.DoesNotExist:
            raise Http404("Team does not exist")
        template = loader.get_template('GUI/team.html')
        context = {
                'team': team_data,
        }
        return HttpResponse(template.render(context, request))

    else:
        # start OpenCV stuff here

        test_function()
        latest_data_list = TeamData.objects.order_by('-record_date')[:5]
        template = loader.get_template('GUI/index.html')
        context = {
                'latest_data_list': latest_data_list,
        }
        return HttpResponse(template.render(context, request))

def index(request):
    return HttpResponse("Index")

def match_details(request, event_id, this_match_number):
    try:
        this_event = event.objects.get(id=event_id)
    except event.DoesNotExist:
        return HttpResponse("Event not found") # improve to return actual html

    this_match = matchResult.objects.filter(linked_event=this_event).filter(match_number=this_match_number).order_by('linked_team__number') # List of all matches from event that match the number
    
    context = {
        'latest_match_list': this_match, 'event_name': this_event.name, 'match_number': this_match[:1].get().match_number
    }

    return render(request, 'GUI/matchDetails.html', context)

def team_details(request, team_number):
    response = "You're looking at the aggregated results for team %s"
    return HttpResponse(response % team_number)

def team_at_event(request, event_id, team_number):

    this_event = event.objects.get(id=event_id)
    this_team = team.objects.get(number=team_number)

    latest_match_list = matchResult.objects.filter(linked_event=this_event).filter(linked_team=this_team).order_by('recorded_time')

    context = {'latest_match_list': latest_match_list, 'event_name': "at " + this_event.name, 'team_number': this_team.number, 'team_name': this_team.name}
    return render(request, 'GUI/teamDetails.html', context)

def team_on_match(request, event_id, team_number, this_match_number):

    this_event = event.objects.get(id=event_id)
    this_team = team.objects.get(number=team_number)

    response = "You're looking at the results for team %s for match %s at event %s"
    return HttpResponse(response % (this_team.number, this_match_number, this_event.name))

def event_details(request, event_id):

    this_event = event.objects.get(id=event_id)

    latest_match_list = matchResult.objects.filter(linked_event=this_event).order_by('match_number')

    unique_match_list = latest_match_list.values_list('match_number').distinct()

    attending_teams = registration.objects.filter(registered_event=this_event).order_by('registered_team__number')

    context = {'latest_match_list': latest_match_list, 'event_name': this_event.name, 'attending_teams': attending_teams, 'unique_match_list': unique_match_list}
    return render(request, 'GUI/event.html', context)

def event_list(request):
    latest_event_list = event.objects.order_by('start_date')

    context = {'latest_event_list': latest_event_list}
    return render(request, 'GUI/event_list.html', context)

def test(request):
    getData()
    return HttpResponse("OH YEAH")