# Generated by Django 3.1.3 on 2021-02-13 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0053_auto_20210212_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(default='Player', max_length=255, verbose_name='Player Name'),
        ),
    ]