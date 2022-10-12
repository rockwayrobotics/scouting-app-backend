from django.db import models

class TeamData(models.Model):
    id = models.IntegerField(primary_key=True) # team ID
    name = models.CharField(max_length=200) # name of the team
    record_date = models.DateField() # when the data was recorded

    def __str__(self):
        return str(self.id)
