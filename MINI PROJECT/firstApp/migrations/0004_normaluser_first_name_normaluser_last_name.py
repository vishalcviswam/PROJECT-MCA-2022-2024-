# Generated by Django 5.0a1 on 2023-10-01 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0003_alter_collegeuser_college_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='normaluser',
            name='first_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='normaluser',
            name='last_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
