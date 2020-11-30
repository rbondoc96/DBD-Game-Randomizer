# Generated by Django 3.1.3 on 2020-11-20 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0022_auto_20201120_0030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('Survivor', 'Survivor'), ('Killer', 'Killer')], max_length=15)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.character')),
                ('effects', models.ManyToManyField(to='game.Effect')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.item')),
                ('item_addons', models.ManyToManyField(null=True, to='game.ItemAddOn')),
                ('offering', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.offering')),
                ('perks', models.ManyToManyField(to='game.Perk')),
                ('power', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.power')),
                ('power_addons', models.ManyToManyField(null=True, to='game.PowerAddOn')),
            ],
        ),
    ]
