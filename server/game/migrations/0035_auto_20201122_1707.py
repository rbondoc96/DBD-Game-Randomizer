# Generated by Django 3.1.3 on 2020-11-23 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0034_auto_20201122_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='effects',
            field=models.ManyToManyField(blank=True, to='game.Effect'),
        ),
        migrations.AlterField(
            model_name='player',
            name='player_id',
            field=models.CharField(default='XSGPF35D', max_length=8, verbose_name='Player ID'),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_id',
            field=models.CharField(default='M7RKIH', max_length=6, unique=True, verbose_name='Session ID'),
        ),
    ]
