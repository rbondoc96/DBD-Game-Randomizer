# Generated by Django 3.1.3 on 2020-11-10 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20201110_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='offering',
            name='quote',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]