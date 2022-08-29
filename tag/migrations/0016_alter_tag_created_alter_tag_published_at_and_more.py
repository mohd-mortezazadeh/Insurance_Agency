# Generated by Django 4.0.1 on 2022-08-04 06:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0015_alter_tag_slug_alter_tag_status_alter_tag_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='published_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش'),
        ),
    ]