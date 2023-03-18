import json
import threading
from datetime import datetime, time
from django.http import HttpResponse
from django.views import View
from django.template import loader
from django.shortcuts import render

from .models import MatchResult, Event, Team, Registration

from .opencv import exe
from .algorithms import generate_rankedteam, analyze_data


def index(request):
    template = loader.get_template("scouting_app/index.html")
    return HttpResponse(template.render())


def match_details(request, event_id, this_match_number):
    try:
        this_event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponse("Event not found")  # improve to return actual html

    this_match = (
        MatchResult.objects.filter(linked_event=this_event)
        .filter(match_number=this_match_number)
        .order_by("linked_team__number")
    )  # List of all matches from event that match the number

    blueAllianceScore = 0
    redAllianceScore = 0

    for teamResult in this_match:
        if teamResult.alliance == "red" and redAllianceScore == 0:
            redAllianceScore = teamResult.alliance_final_score
        if teamResult.alliance == "blue" and blueAllianceScore == 0:
            blueAllianceScore = teamResult.alliance_final_score

    if redAllianceScore > blueAllianceScore:
        winningTeam = "Red"
    else:
        winningTeam = "Blue"

    nextMatchNumber = this_match_number + 1
    prevMatchNumber = this_match_number - 1
    eventNumber = this_event.id

    context = {
        "latest_match_list": this_match,
        "event": this_event,
        "event_number": eventNumber,
        "match_number": this_match_number,
        "b_score": blueAllianceScore,
        "r_score": redAllianceScore,
        "winner": winningTeam,
        "nextMatch": nextMatchNumber,
        "prevMatch": prevMatchNumber,
    }

    return render(request, "scouting_app/matchDetails.html", context)


def team_details(request, team_number):
    this_team = Team.objects.get(number=team_number)

    event_list = Registration.objects.filter(
        registered_team__number=team_number
    ).order_by("registered_event__start_date")

    match_list = MatchResult.objects.filter(linked_team=this_team).order_by(
        "recorded_time"
    )

    context = {"team": this_team, "events": event_list, "matches": match_list}
    return render(request, "scouting_app/teamDetails.html", context)


def team_at_event(request, event_id, team_number):
    this_event = Event.objects.get(id=event_id)
    this_team = Team.objects.get(number=team_number)

    latest_match_list = (
        MatchResult.objects.filter(linked_event=this_event)
        .filter(linked_team=this_team)
        .order_by("recorded_time")
    )

    context = {
        "latest_match_list": latest_match_list,
        "event_name": "at " + this_event.name,
        "team": this_team,
    }
    return render(request, "scouting_app/teamDetails.html", context)


def team_on_match(request, event_id, team_number, this_match_number):
    this_event = Event.objects.get(id=event_id)
    this_team = Team.objects.get(number=team_number)

    context = {
        "team": this_team,
        "event": this_event,
        "match_number": this_match_number,
    }
    return render(request, "scouting_app/teamMatchDetails.html", context)


def event_details(request, event_id):
    this_event = Event.objects.get(id=event_id)

    latest_match_list = MatchResult.objects.filter(linked_event=this_event).order_by(
        "match_number"
    )

    unique_match_list = latest_match_list.values_list("match_number").distinct()

    attending_teams = Registration.objects.filter(registered_event=this_event).order_by(
        "registered_team__number"
    )

    context = {
        "latest_match_list": latest_match_list,
        "event": this_event,
        "attending_teams": attending_teams,
        "unique_match_list": unique_match_list,
    }
    return render(request, "scouting_app/event.html", context)


def event_list(request):
    latest_event_list = Event.objects.order_by("start_date")

    context = {"latest_event_list": latest_event_list}
    return render(request, "scouting_app/event_list.html", context)


def team_list(request):
    teams_list = Team.objects.order_by("number")

    context = {"teams": teams_list}
    return render(request, "scouting_app/team_list.html", context)


def scan(request):
    if request.method == "POST":
        form_data = dict(request.POST)
        del form_data["csrfmiddlewaretoken"]

        # Dump data from form to JSON to send back to JS for field population
        context = {"form_dict": json.dumps(form_data)}

        # If entry doesn't exist, read data from form and save to DB
        if (
            not MatchResult.objects.filter(
                match_number=int(form_data["match_number"][0])
            )
            .filter(
                linked_team=Team.objects.get(number=int(form_data["linked_team"][0]))
            )
            .exists()
        ):
            MatchResult(
                match_number=int(form_data["match_number"][0]),
                linked_team=Team.objects.get(number=int(form_data["linked_team"][0])),
                linked_event=Event.objects.get(event_key=form_data["linked_event"][0]),
                alliance=form_data["alliance"][0],
                auto_balance=bool(int(form_data["auto_balance"][0])),
                auto_move=bool(int(form_data["auto_move"][0])),
                teleop_balance=bool(int(form_data["teleop_balance"][0])),
                parked=bool(int(form_data["parked"][0])),
                endgame_score=int(form_data["endgame_score"][0]),
                endgame_time=float(form_data["endgame_time"][0]),
                penalty=int(form_data["penalty"][0]),
                disabled=bool(int(form_data["disabled"][0])),
                alliance_final_score=int(form_data["alliance_final_score"][0]),
                scouter_comments=form_data["scouter_comments"][0],
                recorded_time=datetime.utcfromtimestamp(
                    int(form_data["recorded_time"][0])
                ),
                cycle_time=time.fromisoformat("04:23:01"),
                pickup_time=time.fromisoformat("04:23:01"),
            ).save()
        else:
            print("match result already exists")

        return render(request, "scouting_app/scan.html", context)

    else:
        # Provide an empty form_dict to prevent JS errors on page load
        context = {"form_dict": {}}

        return render(request, "scouting_app/scan.html", context)


def entry_page(request):
    return render(request, "scouting_app/Entry-page.html")


def events_schedule(request):
    return render(request, "scouting_app/Events-schedule.html")


def matches_schedule(request):
    return render(request, "scouting_app/Matches-schedule.html")


def team_stats(request):
    return render(request, "scouting_app/Team-stats.html")


def match_stats(request):
    return render(request, "scouting_app/Match-stats.html")


def vis_test(request):
    exe()
    return HttpResponse("Beans")


def rank(request):
    match_list = MatchResult.objects.order_by("recorded_time")

    teams_list = Team.objects.order_by("number")
    print(teams_list[0].width)
    # ranked_teams = map(generate_rankedteam, teams_list)
    # threading.Thread(target=analyze_data, args=(match_list,)).start()

    context = {"teams": teams_list}
    return render(request, "scouting_app/rank.html", context)
