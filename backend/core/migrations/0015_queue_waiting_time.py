# Generated by Django 4.0.3 on 2023-06-13 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_ticket_waiting_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='waiting_time',
            field=models.FloatField(default=0.0),
        ),
    ]
