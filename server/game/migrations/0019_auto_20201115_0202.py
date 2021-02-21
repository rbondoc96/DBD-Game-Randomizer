# Generated by Django 3.1.3 on 2020-11-15 10:02

from django.db import migrations, models
import game.models.add_on
import game.models.offering
import game.models.power
import game.storage


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_item_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemaddon',
            name='template',
            field=models.ImageField(blank=True, null=True, storage=game.storage.OverwriteStorage(), upload_to=game.models.add_on.template_item_directory_path),
        ),
        migrations.AddField(
            model_name='offering',
            name='template',
            field=models.ImageField(blank=True, null=True, storage=game.storage.OverwriteStorage(), upload_to=game.models.offering.template_directory_path),
        ),
        migrations.AddField(
            model_name='power',
            name='template',
            field=models.ImageField(blank=True, null=True, storage=game.storage.OverwriteStorage(), 
            upload_to=game.models.power.primary_template_directory_path),
        ),
        migrations.AddField(
            model_name='poweraddon',
            name='template',
            field=models.ImageField(blank=True, null=True, storage=game.storage.OverwriteStorage(), upload_to=game.models.add_on.template_power_directory_path),
        ),
    ]
