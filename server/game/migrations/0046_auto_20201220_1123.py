# Generated by Django 3.1.3 on 2020-12-20 19:23

from django.db import migrations, models
import game.models.power
import game.storage


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0045_auto_20201220_1122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='power',
            old_name='image',
            new_name='primary_image',
        ),
        migrations.AddField(
            model_name='power',
            name='secondary_overlay',
            field=models.ImageField(blank=True, null=True, storage=game.storage.OverwriteStorage(), upload_to=game.models.power.secondary_overlay_directory_path),
        ),
    ]
