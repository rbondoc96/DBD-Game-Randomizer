# Generated by Django 3.1.3 on 2021-03-20 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0068_auto_20210320_1222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offering',
            old_name='quote',
            new_name='flavor',
        ),
    ]
