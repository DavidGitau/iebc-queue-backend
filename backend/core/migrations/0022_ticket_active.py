# Generated by Django 4.0.3 on 2023-07-08 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_queue_current_voter_st'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
