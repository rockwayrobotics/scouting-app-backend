# Generated by Django 4.1.7 on 2023-03-09 21:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("scouting_app", "0016_alter_matchresult_alliance"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="matchresult",
            name="auto_score",
        ),
        migrations.RemoveField(
            model_name="matchresult",
            name="teleop_score",
        ),
        migrations.RemoveField(
            model_name="matchresult",
            name="tippy",
        ),
        migrations.AddField(
            model_name="matchresult",
            name="auto_balance",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="matchresult",
            name="cycle_time",
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="matchresult",
            name="parked",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="matchresult",
            name="pickup_time",
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="matchresult",
            name="teleop_balance",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="team",
            name="average_scoring_time",
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="team",
            name="pickup_locations",
            field=models.BinaryField(default=b"\x08"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="team",
            name="scoring_consistency",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="team",
            name="scoring_locations",
            field=models.BinaryField(default=b"\x08"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="team",
            name="swerve",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="team",
            name="tippy",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="team",
            name="width",
            field=models.FloatField(default=0),
        ),
    ]
