# Generated by Django 5.1.2 on 2024-11-29 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0019_activitynew_max_participants"),
    ]

    operations = [
        migrations.AddField(
            model_name="activitynew",
            name="current_participants",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]