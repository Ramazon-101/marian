# Generated by Django 4.1.3 on 2022-11-15 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_rename_day_rooms_duration_alter_rooms_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rooms',
            name='duration',
        ),
    ]
