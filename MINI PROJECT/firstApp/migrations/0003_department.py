# Generated by Django 5.0a1 on 2023-10-26 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0002_normaluser_first_name_normaluser_last_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('undergrad_offered', models.BooleanField(default=False)),
                ('postgrad_offered', models.BooleanField(default=False)),
                ('head_of_department', models.CharField(max_length=255)),
                ('department_start_year', models.PositiveIntegerField()),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstApp.collegeuser')),
            ],
        ),
    ]
