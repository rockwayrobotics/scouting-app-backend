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
