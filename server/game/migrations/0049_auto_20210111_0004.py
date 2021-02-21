# Generated by Django 3.1.3 on 2021-01-11 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0048_auto_20201220_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConditionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ModifierType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ModifierUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='effect',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='Modifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('value', models.IntegerField()),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.modifiertype')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.modifierunit')),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.event')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.conditiontype')),
            ],
        ),
        migrations.AddField(
            model_name='effect',
            name='condition',
            field=models.ManyToManyField(to='game.Condition'),
        ),
        migrations.AddField(
            model_name='effect',
            name='modifiers',
            field=models.ManyToManyField(to='game.Modifier'),
        ),
    ]
