# Generated by Django 4.0.1 on 2023-05-05 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_hits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='hits',
        ),
    ]
