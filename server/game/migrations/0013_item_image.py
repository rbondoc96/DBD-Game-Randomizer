# Generated by Django 3.1.3 on 2020-11-14 21:57

from django.db import migrations, models
import game.models.item
import game.storage


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_offering_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=game.storage.OverwriteStorage(), upload_to=game.models.item.item_directory_path),
        ),
    ]
