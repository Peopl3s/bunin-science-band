# Generated by Django 4.2.2 on 2023-06-23 15:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0004_news_image_alter_news_publish"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="publish",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 6, 23, 15, 54, 39, 67268, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
