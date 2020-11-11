# Generated by Django 3.1.3 on 2020-11-10 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_offering_quote'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Item Type',
                'verbose_name_plural': 'Item Types',
            },
        ),
        migrations.AlterModelOptions(
            name='rarity',
            options={'verbose_name_plural': 'Rarities'},
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('quote', models.CharField(blank=True, max_length=255, null=True)),
                ('effects', models.ManyToManyField(to='game.Effect', verbose_name='Effects')),
                ('rarity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.rarity')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.itemtype')),
            ],
        ),
    ]