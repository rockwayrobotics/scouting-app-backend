from django.core.management.base import BaseCommand, CommandError

import requests
import json
import os

from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

from scouting_app.models import MatchResult, Event, Team, Registration

my_headers = {"X-TBA-Auth-Key": os.getenv('TBA_AUTH')}


class Command(BaseCommand):
    help = "Pulls data from TBA API for setup of matches and events"

    def add_arguments(self, parser):
        parser.add_argument('--id', nargs='*')
        parser.add_argument('--year', nargs='?', default=datetime.now().year, const=datetime.now().year, type=int)

    def handle(self, *args, **options):
        print(f"ID: {options['id']}")
        print(f"YEAR: {options['year']}")

        result = json.loads(requests.get("https://www.thebluealliance.com/api/v3/team/frc8089/events/simple", headers=my_headers).text)

        for i in result:
            if i['year'] == options['year']:
                print(i['key'] + " - " + i['name'])
                if not Event.objects.filter(event_key=i['key']).exists():
                    Event(
                        name = i['name'],
                        start_date = i['start_date'],
                        end_date = i['end_date'],
                        event_key = i['key'],
                    ).save()

                result = json.loads(requests.get(f"https://www.thebluealliance.com/api/v3/event/{i['key']}/teams", headers=my_headers).text)

                for item in result:
                    if not Team.objects.filter(number=item['team_number']).exists():
                        Team(
                            number = item['team_number'],
                            name = item['nickname']
                        ).save()
                    
                    if not Registration.objects.filter(registered_team = Team.objects.get(number=item['team_number']), registered_event = Event.objects.get(event_key=i['key'])).exists():
                        Registration(
                            registered_team = Team.objects.get(number=item['team_number']),
                            registered_event = Event.objects.get(event_key=i['key'])
                        ).save()

                    print("Team " + str(item['team_number']) + " - " + item['nickname'])
