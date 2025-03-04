# Generated by Django 4.2.16 on 2024-11-17 05:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0006_activitynew_check_status_sponsorshipnew_check_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorshipnew',
            name='organizer',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='organized_activities', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
