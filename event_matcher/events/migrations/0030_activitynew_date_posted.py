# Generated by Django 5.1.2 on 2024-12-02 15:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0029_alter_activitynew_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="activitynew",
            name="date_posted",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]