# Generated by Django 4.1.2 on 2022-10-24 20:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("scouting_app", "0009_alter_matchresult_recorded_time"),
    ]

    operations = [
        migrations.RenameField(
            model_name="matchresult",
            old_name="event",
            new_name="linked_event",
        ),
        migrations.RenameField(
            model_name="matchresult",
            old_name="team",
            new_name="linked_team",
        ),
    ]
