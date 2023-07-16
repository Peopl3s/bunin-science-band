# Generated by Django 4.2.2 on 2023-06-23 15:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0003_rename_post_comment_news_alter_news_publish"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="image",
            field=models.ImageField(blank=True, upload_to="users/%Y/%m/%d/"),
        ),
        migrations.AlterField(
            model_name="news",
            name="publish",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 6, 23, 15, 52, 23, 19778, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]