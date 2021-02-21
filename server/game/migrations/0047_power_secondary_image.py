# Generated by Django 3.1.3 on 2020-12-20 19:24

from django.db import migrations, models
import game.models.power
import game.storage


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0046_auto_20201220_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='power',
            name='secondary_image',
            field=models.ImageField(blank=True, null=True, storage=game.storage.OverwriteStorage(), upload_to=game.models.power.secondary_power_directory_path),
        ),
    ]
