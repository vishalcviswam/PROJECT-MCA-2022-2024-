# Generated by Django 5.0a1 on 2023-11-01 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0009_remove_course_course_tags_remove_course_exam_types_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CourseTag',
        ),
        migrations.DeleteModel(
            name='ExamType',
        ),
        migrations.DeleteModel(
            name='Language',
        ),
    ]