# Generated by Django 4.0.6 on 2023-06-13 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_location_skills'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='skills',
            new_name='Skill',
        ),
    ]
