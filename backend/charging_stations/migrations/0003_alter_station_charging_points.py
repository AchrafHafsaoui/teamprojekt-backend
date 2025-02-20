from django.db import migrations, models
import json

def migrate_charging_points(apps, schema_editor):
    Station = apps.get_model("charging_stations", "Station")
    for station in Station.objects.all():
        # Convert existing integer[] to JSON format (set all to null)
        station.charging_points = [None] * len(station.charging_points) if station.charging_points else []
        station.save()

class Migration(migrations.Migration):

    dependencies = [
        ("charging_stations", "0002_station_charging_points"),  # Adjust based on your last migration
    ]

    operations = [
        migrations.AddField(
            model_name="station",
            name="charging_points_new",
            field=models.JSONField(default=list),
        ),
        migrations.RunPython(migrate_charging_points),
        migrations.RemoveField(model_name="station", name="charging_points"),
        migrations.RenameField(model_name="station", old_name="charging_points_new", new_name="charging_points"),
    ]
