# Generated by Django 4.0.6 on 2023-06-18 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['is_read', '-created']},
        ),
    ]
