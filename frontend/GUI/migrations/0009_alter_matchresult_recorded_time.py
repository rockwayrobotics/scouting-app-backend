# Generated by Django 4.1.2 on 2022-10-22 01:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GUI', '0008_matchresult_disabled_matchresult_scouter_comments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchresult',
            name='recorded_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
