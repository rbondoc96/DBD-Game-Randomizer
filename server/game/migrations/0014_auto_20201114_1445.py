# Generated by Django 3.1.3 on 2020-11-14 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_item_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AddOn',
            new_name='ItemAddOn',
        ),
        migrations.AlterModelOptions(
            name='itemaddon',
            options={'verbose_name': 'Item Add-On', 'verbose_name_plural': 'Item Add-Ons'},
        ),
    ]
