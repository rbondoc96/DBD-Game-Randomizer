# Generated by Django 3.1.3 on 2020-11-14 23:28

from django.db import migrations, models
import game.models.add_on
import game.storage


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_auto_20201114_1515'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='power',
            options={'ordering': ['owner']},
        ),
        migrations.AddField(
            model_name='itemaddon',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=game.storage.OverwriteStorage(), upload_to=game.models.add_on.item_addon_directory_path),
        ),
        migrations.AddField(
            model_name='poweraddon',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=game.storage.OverwriteStorage(), upload_to=game.models.add_on.power_addon_directory_path),
        ),
    ]
