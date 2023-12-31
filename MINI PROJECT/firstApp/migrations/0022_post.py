# Generated by Django 5.0a1 on 2023-11-21 23:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0021_alter_courseprogress_course_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/images/')),
                ('video', models.FileField(blank=True, null=True, upload_to='posts/videos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('college_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstApp.collegeuser')),
            ],
        ),
    ]
