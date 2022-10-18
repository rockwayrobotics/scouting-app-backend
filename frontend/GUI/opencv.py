from .models import TeamData
from django.utils import timezone

def test_function():
    print("Doing some vision code")

    team_number = 1
    team_name = "Test"
    record_date = timezone.now()
    driving_skill = 0.0
    died = True
    tipped = True
    points_scored = 0
    comments = "test team comment"
    safety_concerns = "N" # See models.py for list of concerns

    new_team_data = TeamData(id=team_number,name=team_name,record_date=record_date,driving_skill=driving_skill,died=died,tipped=tipped,points_scored=points_scored,comments=comments,safety_concerns=safety_concerns)

    new_team_data.save()
