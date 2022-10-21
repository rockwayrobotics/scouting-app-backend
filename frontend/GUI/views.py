from django.http import HttpResponse
from django.views import View
from django.template import loader
from django.shortcuts import render

from .models import TeamData, matchResult, event
from .opencv import test_function

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

def match_details(request, event_id, match_number):
    try:
        this_event = event.objects.get(id=event_id)
    except event.DoesNotExist:
        return HttpResponse("Event not found") # improve to return actual html

    this_match = matchResult.objects.filter(event=this_event).filter(id=match_number).order_by('team_number') # List of all matches from event that match the number
    
    context = {
        'latest_match_list': this_match, 'event_name': this_event.name, 'match_number': match_number
    }

    # response = "You're looking at the results of match %s at event %s"
    # return HttpResponse(response % (match_number, event_id))

    return render(request, 'scoutingApp/matchDetails.html', context)

def team_details(request, team_number):
    response = "You're looking at the aggregated results for team %s"
    return HttpResponse(response % team_number)

def team_at_event(request, event_id, team_number):
    response = "You're looking at the event results for team %s at event %s"
    return HttpResponse(response % (team_number, event_id))

def team_on_match(request, event_id, team_number, match_number):
    response = "You're looking at the results for team %s for match %s at event %s"
    return HttpResponse(response % (team_number, match_number, event_id))

def event_details(request, event_id):

    this_event = event.objects.get(id=event_id)

    latest_match_list = matchResult.objects.filter(event=this_event).order_by('recorded_time')

    context = {'latest_match_list': latest_match_list, 'event_name': this_event.name}
    return render(request, 'scoutingApp/index.html', context)

def scan_code(request):
    return render(request, 'scoutingApp/scan.html')

# TODO Read data from QR code using button on website, presumably redirect via html from template? not sure. Also consider paramaters via url, with button to add to DB
# 
