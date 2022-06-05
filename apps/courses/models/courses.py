from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.models import BaseModel

from .reviews import get_sentinel_user


def get_directory_path(instance) -> str:
    """Get directory for save image of course."""
    return f"course_{instance.name}_{instance.id}"


class Course(BaseModel):
    """Model for Course."""

    name = models.CharField(
        max_length=128,
        verbose_name=_("Name of course"),
    )
    description = models.TextField(
        verbose_name=_("Description of course"),
    )
    image = models.ImageField(
        upload_to=get_directory_path,
        verbose_name=_("Image of course"),
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=11,
        verbose_name=_("Price of course"),
        null=True,
        blank=True,
    )
    students = models.ManyToManyField(
        "apps.users.User",
        verbose_name=_("One of students"),
        related_name="courses",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        verbose_name=_("Category of course"),
        related_name="courses",
    )

    class Meta:
        verbose_name_plural = _("Courses")
        verbose_name = _("Course")


class Category(BaseModel):
    """Model for Category."""

    name = models.CharField(
        max_length=128,
        verbose_name=_("Name of category"),
    )

    class Meta:
        verbose_name_plural = _("Categories")
        verbose_name = _("Category")


class Topic(BaseModel):
    """Model for Topic."""

    title = models.CharField(verbose_name=_("One title of topic"))
    number = models.IntegerField(
        verbose_name=_("Number topic in course"),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=_("Course for topic"),
        related_name="topics",
    )

    class Meta:
        verbose_name_plural = _("Topics")
        verbose_name = _("Topic")


class Task(BaseModel):
    """Model for Task.

    Task types:
        Information: in body of task exist only some information
        Test: in body of task exist information and questions
    """

    class Type(models.TextChoices):
        """Class choices."""

        INFORMATION = "INFORMATION", _("Information")
        TEST = "TEST", _("Test")

    type = models.CharField(
        verbose_name=_("Type"),
        choices=Type.choices,
    )
    title = models.CharField(verbose_name=_("One title of task"))
    text = models.TextField(
        verbose_name=_("Text or description"),
    )

    class Meta:
        verbose_name_plural = _("Tasks")
        verbose_name = _("Task")


class Answer(BaseModel):
    """Model for Question."""

    is_true = models.BooleanField(
        verbose_name=_("Is true answer"),
        default=False,
    )
    content = models.TextField(
        verbose_name=_("Content of answer"),
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_("Task of answers"),
        related_name="answers",
    )

    class Meta:
        verbose_name_plural = _("Answers")
        verbose_name = _("Answer")


class Comment(BaseModel):
    """Model for Comment."""

    content = models.TextField(
        verbose_name=_("Content of comment"),
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_("Task of comment"),
        related_name="comments",
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Parent comment"),
        related_name="child_comments",
    )
    user = models.ForeignKey(
        "apps.users.User",
        on_delete=models.SET(get_sentinel_user),
        verbose_name=_("Owner of comment"),
    )

    class Meta:
        verbose_name_plural = _("Comments")
        verbose_name = _("Comment")
