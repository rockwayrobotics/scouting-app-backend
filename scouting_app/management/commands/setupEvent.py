import requests
import json
import os
from configparser import ConfigParser

from django.core.management.base import BaseCommand
from django.utils import timezone

from scouting_app.models import MatchResult, Event, Team, Registration

if os.getenv("TBA_AUTH") is not None:
    my_headers = {"X-TBA-Auth-Key": os.getenv("TBA_AUTH")}

elif os.path.exists("settings.ini"):
    config = ConfigParser()
    config.read("settings.ini")
    try:
        my_headers = {"X-TBA-Auth-Key": config["settings"]["tba_auth"]}

    except KeyError:
        print(
            "ERROR: TBA API key could not be loaded from settings.ini, is the file formatted correctly? Aborting."
        )
        exit()
else:
    print(
        "ERROR: TBA API key could not be located in environment variables or settings.ini. Aborting."
    )


def registerTeam(team_number, event_item, team_list):
    # print(f"Team {team_number} registered")
    if not Team.objects.filter(number=team_number).exists():
        for team_item in team_list:
            if team_item["team_number"] == int(team_number):
                Team(number=team_number, name=team_item["nickname"]).save()

    if not Registration.objects.filter(
        registered_team=Team.objects.get(number=team_number),
        registered_event=Event.objects.get(event_key=event_item["key"]),
    ).exists():
        Registration(
            registered_team=Team.objects.get(number=team_number),
            registered_event=Event.objects.get(event_key=event_item["key"]),
        ).save()


def registerMatch(event_item, team_number, match_item, alliance_colour):
    if not MatchResult.objects.filter(
        linked_event=Event.objects.get(event_key=event_item["key"]),
        linked_team=Team.objects.get(number=team_number),
        match_number=match_item["match_number"],
    ).exists():
        # print(f"Match {match_item['match_number']} - Team {team_number} - {alliance_colour} alliance")

        MatchResult(
            match_number=match_item["match_number"],
            linked_team=Team.objects.get(number=team_number),
            linked_event=Event.objects.get(event_key=event_item["key"]),
            alliance=alliance_colour,
            recorded_time=timezone.now(),
            auto_balance=False,
            auto_move=False,
            teleop_balance=False,
            endgame_score=0,
            parked=False,
            endgame_time=0,
            penalty=0,
            disabled=False,
            cycle_time=timezone.now(),
            pickup_time=timezone.now(),
            alliance_final_score=match_item["alliances"][alliance_colour]["score"],
        ).save()


def process_event(event_item):
    print(f"Processing {event_item['key']} - {event_item['name']}")
    if not Event.objects.filter(event_key=event_item["key"]).exists():
        Event(
            name=event_item["name"],
            start_date=event_item["start_date"],
            end_date=event_item["end_date"],
            event_key=event_item["key"],
        ).save()

    registered_teams = []

    team_list = json.loads(
        requests.get(
            f"https://www.thebluealliance.com/api/v3/event/{event_item['key']}/teams",
            headers=my_headers,
        ).text
    )

    match_list = json.loads(
        requests.get(
            f"https://www.thebluealliance.com/api/v3/event/{event_item['key']}/matches/simple",
            headers=my_headers,
        ).text
    )

    for match_item in match_list:
        if match_item["comp_level"] == "qm":
            for team_number in match_item["alliances"]["blue"]["team_keys"]:
                alliance_colour = "blue"
                if (
                    not team_number in registered_teams
                ):  # Don't re-register teams if we already know they're registered
                    registerTeam(team_number[3:], event_item, team_list)
                    registered_teams.append(team_number)
                registerMatch(event_item, team_number[3:], match_item, alliance_colour)
            for team_number in match_item["alliances"]["red"]["team_keys"]:
                alliance_colour = "red"
                if (
                    not team_number in registered_teams
                ):  # Don't re-register teams if we already know they're registered
                    registerTeam(team_number[3:], event_item, team_list)
                    registered_teams.append(team_number)
                registerMatch(event_item, team_number[3:], match_item, alliance_colour)


class Command(BaseCommand):
    help = "Pulls data from TBA API for setup of matches and events"

    def add_arguments(self, parser):
        parser.add_argument("--key", nargs="*")
        parser.add_argument("--year", nargs="*", type=int)

    def handle(self, *args, **options):
        print(f"EVENT KEY: {options['key']}")
        print(f"YEAR: {options['year']}")

        event_found = False

        event_list = json.loads(
            requests.get(
                "https://www.thebluealliance.com/api/v3/team/frc8089/events/simple",
                headers=my_headers,
            ).text
        )

        for event_item in event_list:
            if options["year"] == None and options["key"] == None:
                process_event(event_item)
                event_found = True

            elif (
                options["year"] == None
                and not options["key"] == None
                and event_item["key"] == options["key"][0]
            ):
                process_event(event_item)
                event_found = True

            elif (
                not options["year"] == None
                and options["key"] == None
                and event_item["year"] == options["year"][0]
            ):
                process_event(event_item)
                event_found = True

            elif (
                not options["year"] == None
                and not options["key"] == None
                and event_item["year"] == options["year"][0]
                and event_item["key"] == options["key"][0]
            ):
                process_event(event_item)
                event_found = True

        if not event_found:
            print("No event found for criteria")
