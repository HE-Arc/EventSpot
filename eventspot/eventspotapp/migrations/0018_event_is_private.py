# Generated by Django 4.0.2 on 2022-03-14 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventspotapp', '0017_alter_event_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
