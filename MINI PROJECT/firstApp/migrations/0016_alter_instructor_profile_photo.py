# Generated by Django 5.0a1 on 2023-11-07 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0015_instructor_profile_photo_instructor_qualification_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photo/'),
        ),
    ]