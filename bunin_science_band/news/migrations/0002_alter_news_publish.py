# Generated by Django 4.2.2 on 2023-06-23 03:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="publish",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 6, 23, 3, 55, 48, 354011, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
