# Generated by Django 3.1.3 on 2020-11-10 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20201110_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='image',
            field=models.ImageField(null=True, upload_to='media/characters'),
        ),
    ]
