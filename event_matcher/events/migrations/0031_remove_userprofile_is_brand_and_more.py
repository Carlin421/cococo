# Generated by Django 4.2.16 on 2024-12-02 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0030_userprofile_is_brand_userprofile_is_club'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_brand',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='is_club',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(blank=True, choices=[('brand', '品牌方'), ('club', '社團方')], max_length=20),
        ),
    ]