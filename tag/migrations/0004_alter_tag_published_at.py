# Generated by Django 4.0.1 on 2022-02-10 22:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0003_auto_20220210_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='published_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 10, 22, 30, 27, 828387, tzinfo=utc)),
        ),
    ]
