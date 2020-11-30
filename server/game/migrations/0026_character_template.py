# Generated by Django 3.1.3 on 2020-11-22 01:31

from django.db import migrations, models
import game.models.character
import game.storage


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0025_auto_20201121_0317'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='template',
            field=models.ImageField(blank=True, null=True, storage=game.storage.OverwriteStorage(), upload_to=game.models.character.template_directory_path),
        ),
    ]
