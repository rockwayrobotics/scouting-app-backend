# Generated by Django 4.1.2 on 2022-10-22 01:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scouting_app", "0007_remove_matchresult_team_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="matchresult",
            name="disabled",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="matchresult",
            name="scouter_comments",
            field=models.CharField(default="", max_length=500),
        ),
        migrations.AlterField(
            model_name="matchresult",
            name="recorded_time",
            field=models.DateTimeField(
                default=datetime.datetime(2022, 10, 21, 20, 48, 38, 566515)
            ),
        ),
    ]
