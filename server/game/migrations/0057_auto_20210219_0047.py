# Generated by Django 3.1.3 on 2021-02-19 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0056_remove_player_effects'),
    ]

    operations = [
        migrations.RenameField(
            model_name='effect',
            old_name='condition',
            new_name='conditions',
        ),
    ]
