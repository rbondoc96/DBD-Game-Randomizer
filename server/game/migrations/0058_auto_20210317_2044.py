# Generated by Django 3.1.3 on 2021-03-18 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0057_auto_20210219_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perk',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='perk',
            name='effects',
            field=models.ManyToManyField(blank=True, to='game.Effect', verbose_name='Effects'),
        ),
    ]
