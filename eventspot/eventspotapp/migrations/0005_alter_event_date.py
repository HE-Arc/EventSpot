# Generated by Django 4.0.2 on 2022-03-12 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventspotapp', '0004_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(),
        ),
    ]