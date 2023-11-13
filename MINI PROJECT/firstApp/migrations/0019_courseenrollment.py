# Generated by Django 5.0a1 on 2023-11-11 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0018_department_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('enrollment_id', models.AutoField(primary_key=True, serialize=False)),
                ('enrollment_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstApp.course')),
                ('normal_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstApp.normaluser')),
            ],
        ),
    ]
