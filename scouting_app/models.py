import datetime
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    event_key = models.CharField(max_length=9)

    def __str__(self):
        return str(self.name)


class Team(models.Model):
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "Team " + str(self.number)


class Registration(models.Model):
    registered_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    registered_event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return (
            "Team "
            + str(self.registered_team.number)
            + " at event "
            + self.registered_event.name
        )


class MatchResult(models.Model):
    # metadata
    match_number = models.IntegerField(default=0)
    linked_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    linked_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    alliance = models.CharField(max_length=4)
    recorded_time = models.DateTimeField(default=datetime.datetime.now)

    # auto
    auto_score = models.IntegerField(default=0)
    auto_move = models.BooleanField(default=False)

    # teleop
    teleop_score = models.IntegerField(default=0)

    # endgame
    endgame_score = models.IntegerField(default=0)
    endgame_time = models.FloatField(default=0)

    # penalty
    penalty = models.IntegerField(default=0)
    tippy = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)

    alliance_final_score = models.IntegerField(default=0)

    # comments
    scouter_comments = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return (
            "Results - Match "
            + str(self.match_number)
            + " Team "
            + str(self.linked_team.number)
        )


# class pitScout(models.Model):
#     # metadata
