# Generated by Django 3.1.4 on 2020-12-18 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_ticket_passangercontact'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='hearts',
            field=models.FloatField(default=200),
        ),
        migrations.AlterField(
            model_name='seats',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
