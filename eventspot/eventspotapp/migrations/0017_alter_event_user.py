# Generated by Django 4.0.2 on 2022-03-13 22:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eventspotapp', '0016_alter_event_image_alter_event_lattitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
