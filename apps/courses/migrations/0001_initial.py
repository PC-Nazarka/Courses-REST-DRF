# Generated by Django 3.2.13 on 2022-06-14 13:04

import apps.courses.models.courses
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=128, verbose_name="Name of category"),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("DRAFT", "Draft"), ("READY", "Ready")],
                        max_length=255,
                        verbose_name="Status of course",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=128, verbose_name="Name of course"),
                ),
                ("description", models.TextField(verbose_name="Description of course")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=apps.courses.models.courses.get_directory_path,
                        verbose_name="Image of course",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0.0"),
                        max_digits=11,
                        verbose_name="Price of course",
                    ),
                ),
                (
                    "archive_users",
                    models.ManyToManyField(
                        related_name="archive_courses",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Users who add course in archive",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="courses",
                        to="courses.category",
                        verbose_name="Category of course",
                    ),
                ),
                (
                    "interest_users",
                    models.ManyToManyField(
                        related_name="favorite_courses",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Users mean, that this course is interesting",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="courses",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Owner of course",
                    ),
                ),
                (
                    "passers_users",
                    models.ManyToManyField(
                        related_name="pass_courses",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Passes users",
                    ),
                ),
                (
                    "students",
                    models.ManyToManyField(
                        related_name="courses_student",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="One of students",
                    ),
                ),
                (
                    "want_pass_users",
                    models.ManyToManyField(
                        related_name="want_pass_courses",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Users who want pass course",
                    ),
                ),
            ],
            options={
                "verbose_name": "Course",
                "verbose_name_plural": "Courses",
            },
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="One title of topic"),
                ),
                ("number", models.IntegerField(verbose_name="Number topic in course")),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="topics",
                        to="courses.course",
                        verbose_name="Course for topic",
                    ),
                ),
            ],
            options={
                "verbose_name": "Topic",
                "verbose_name_plural": "Topics",
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "type_task",
                    models.CharField(
                        choices=[("INFORMATION", "Information"), ("TEST", "Test")],
                        max_length=255,
                        verbose_name="Type",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="One title of task"),
                ),
                ("text", models.TextField(verbose_name="Text or description")),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="courses.topic",
                        verbose_name="Task of topic",
                    ),
                ),
            ],
            options={
                "verbose_name": "Task",
                "verbose_name_plural": "Tasks",
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("rating", models.IntegerField(verbose_name="Mark of course by user")),
                ("review", models.TextField(verbose_name="Review of course by user")),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="courses.course",
                        verbose_name="Reviews of courses",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=models.SET(
                            apps.courses.models.courses.get_sentinel_user
                        ),
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Owner of review",
                    ),
                ),
            ],
            options={
                "verbose_name": "Review",
                "verbose_name_plural": "Reviews",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("content", models.TextField(verbose_name="Content of comment")),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="child_comments",
                        to="courses.comment",
                        verbose_name="Parent comment",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="courses.task",
                        verbose_name="Task of comment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=models.SET(
                            apps.courses.models.courses.get_sentinel_user
                        ),
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Owner of comment",
                    ),
                ),
            ],
            options={
                "verbose_name": "Comment",
                "verbose_name_plural": "Comments",
            },
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "is_true",
                    models.BooleanField(default=False, verbose_name="Is true answer"),
                ),
                ("content", models.TextField(verbose_name="Content of answer")),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="courses.task",
                        verbose_name="Task of answers",
                    ),
                ),
            ],
            options={
                "verbose_name": "Answer",
                "verbose_name_plural": "Answers",
            },
        ),
    ]
