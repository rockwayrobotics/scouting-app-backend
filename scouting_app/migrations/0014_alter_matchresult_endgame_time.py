# Generated by Django 4.1.2 on 2022-11-12 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scouting_app', '0013_delete_teamdata_alter_event_event_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchresult',
            name='endgame_time',
            field=models.FloatField(default=0),
        ),
    ]