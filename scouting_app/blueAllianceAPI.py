import requests
import json
import os

from django.core.exceptions import ObjectDoesNotExist

from .models import MatchResult, Event, Team, Registration

my_headers = {"X-TBA-Auth-Key": os.getenv('TBA_AUTH')}


def get_data():
    result = json.loads(
        requests.get("https://www.thebluealliance.com/api/v3/team/frc8089/events/simple", headers=my_headers).text)

    for i in result:
        if i['year'] == 2022:
            print(i['key'] + " - " + i['name'])
            try:
                Event.objects.get(event_key=i['key'])
            except ObjectDoesNotExist:
                result = json.loads(
                    requests.get(f"https://www.thebluealliance.com/api/v3/event/{i['key']}/teams", headers=my_headers).text)

                for item in result:
                    print("Team " + str(item['team_number']) + " - " + item['nickname'])