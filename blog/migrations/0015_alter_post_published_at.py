# Generated by Django 3.2.9 on 2022-02-14 15:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_alter_post_published_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 14, 15, 6, 19, 782777, tzinfo=utc)),
        ),
    ]
