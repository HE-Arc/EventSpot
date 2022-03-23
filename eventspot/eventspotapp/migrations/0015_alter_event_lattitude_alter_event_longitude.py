# Generated by Django 4.0.2 on 2022-03-13 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventspotapp', '0014_alter_event_image_alter_event_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='lattitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]