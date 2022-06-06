# Generated by Django 3.2.13 on 2022-06-06 21:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_alter_course_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='courses_student', to=settings.AUTH_USER_MODEL, verbose_name='One of students'),
        ),
    ]