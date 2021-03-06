# Generated by Django 3.1.3 on 2020-11-23 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0038_auto_20201122_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Player Name'),
        ),
        migrations.AlterField(
            model_name='player',
            name='player_id',
            field=models.CharField(default='74CKJLOI', max_length=8, verbose_name='Player ID'),
        ),
        migrations.AlterField(
            model_name='session',
            name='players',
            field=models.ManyToManyField(blank=True, related_name='players', to='game.Player'),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_id',
            field=models.CharField(default='XFLC4G', max_length=6, unique=True, verbose_name='Session ID'),
        ),
    ]
