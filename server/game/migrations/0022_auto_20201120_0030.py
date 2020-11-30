# Generated by Django 3.1.3 on 2020-11-20 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0021_auto_20201115_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='addons',
            field=models.ManyToManyField(to='game.ItemAddOn', verbose_name='Item Add-ons'),
        ),
    ]
