# Generated by Django 4.2 on 2023-05-21 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_rename_station_id_pollingstation_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="pollingstation",
            name="voter_no",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]