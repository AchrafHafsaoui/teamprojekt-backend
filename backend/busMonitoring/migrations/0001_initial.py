# Generated by Django 5.1.3 on 2024-12-03 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElectricBus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(max_length=50)),
                ('bus_id', models.CharField(max_length=50, unique=True)),
                ('battery', models.FloatField()),
                ('charging_start', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('In Depot', 'In Depot'), ('Maintenance', 'Maintenance'), ('On Route', 'On Route')], max_length=20)),
                ('charging_location', models.CharField(blank=True, max_length=50, null=True)),
                ('CAP', models.CharField(max_length=20)),
                ('ENE', models.CharField(max_length=20)),
            ],
        ),
    ]
