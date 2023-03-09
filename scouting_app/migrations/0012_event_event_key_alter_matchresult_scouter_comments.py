# Generated by Django 4.1.2 on 2022-10-25 00:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scouting_app", "0011_registration"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="event_key",
            field=models.CharField(default="", max_length=8),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="matchresult",
            name="scouter_comments",
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
