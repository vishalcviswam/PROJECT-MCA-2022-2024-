# Generated by Django 5.0a1 on 2023-10-30 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0007_coursetag_examtype_language_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_type',
        ),
    ]
