# Generated by Django 3.1.3 on 2020-11-21 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0024_auto_20201121_0316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='item_addons',
            field=models.ManyToManyField(blank=True, to='game.ItemAddOn'),
        ),
        migrations.AlterField(
            model_name='player',
            name='power_addons',
            field=models.ManyToManyField(blank=True, to='game.PowerAddOn'),
        ),
    ]
