# Generated by Django 5.0a1 on 2023-11-06 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0013_fillintheblankquestion_imagequestion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='choices',
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='choice_1',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='choice_2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='choice_3',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='choice_4',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
