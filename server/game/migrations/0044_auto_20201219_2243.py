# Generated by Django 3.1.3 on 2020-12-20 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0043_auto_20201217_0520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='power',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='game.character'),
        ),
    ]