# Generated by Django 5.0a1 on 2023-10-01 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collegeuser',
            name='established_year',
        ),
        migrations.RemoveField(
            model_name='normaluser',
            name='date_of_birth',
        ),
    ]