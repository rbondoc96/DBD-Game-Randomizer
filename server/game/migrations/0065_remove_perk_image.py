# Generated by Django 3.1.3 on 2021-03-20 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0064_auto_20210319_2345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perk',
            name='image',
        ),
    ]
