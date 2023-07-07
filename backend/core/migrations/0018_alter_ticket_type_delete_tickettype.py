# Generated by Django 4.0.3 on 2023-06-25 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_ticket_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='type',
            field=models.CharField(choices=[('S', 'Special'), ('A', 'On Time'), ('B', 'Out of Time')], max_length=1, verbose_name='condition'),
        ),
        migrations.DeleteModel(
            name='TicketType',
        ),
    ]
