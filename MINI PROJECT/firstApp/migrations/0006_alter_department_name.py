# Generated by Django 5.0a1 on 2023-10-30 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0005_instructor_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
