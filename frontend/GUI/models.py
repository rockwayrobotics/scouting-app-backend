import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _

class TeamData(models.Model):
    id = models.IntegerField(primary_key=True) # team ID
    name = models.CharField(max_length=30) # name of the team
    record_date = models.DateField() # when the data was recorded
    
    driving_skill = models.DecimalField(max_digits=3, decimal_places=2) # driver skill from 0-1
    died = models.BooleanField() # if they died or not
    tipped = models.BooleanField() # if they tipped over or not
    points_scored = models.IntegerField() # how many points they scored
    comments = models.CharField(max_length=250) # any driver comments

    class SafetyConcerns(models.TextChoices):
        FIRE = 'F', _('Fire Hazard')
        PNEUMATIC = 'P', _('Pneumatic Hazard')
        ELECTRICAL = 'E', _('Electrical Hazard')
        TIPPING = 'T', _('Tipping Hazard')
        MECHANICAL = 'M', _('Mechanical Hazard')
        NONE = 'N', _('No Concerns')

    safety_concerns = models.CharField(
            max_length=1,
            choices=SafetyConcerns.choices,
            default=SafetyConcerns.NONE,
        ) # any possible safety concerns, from an enum

    def __str__(self):
        return str(self.id)

class event(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.name)
    

class team(models.Model):
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "Team " + str(self.number)

class matchResult(models.Model):
    # metadata
    match_number = models.IntegerField(default=0)
    linked_team = models.ForeignKey(team, on_delete=models.CASCADE)
    linked_event = models.ForeignKey(event, on_delete=models.CASCADE)
    recorded_time = models.DateTimeField(default=datetime.datetime.now)

    # auto
    auto_score = models.IntegerField(default=0)
    auto_move = models.BooleanField(default=False)

    # teleop
    teleop_score = models.IntegerField(default=0)

    # endgame
    endgame_score = models.IntegerField(default=0)
    endgame_time = models.IntegerField(default=0)

    # penalty
    penalty = models.IntegerField(default=0)
    tippy = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)

    # comments
    scouter_comments = models.CharField(max_length=500, default="")

    def __str__(self):
        return "Results - Match " + str(self.match_number) +  " Team " + str(self.team.number)

# class pitScout(models.Model):
#     # metadata
    
