import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.courses import factories, models

pytestmark = pytest.mark.django_db


def test_create_comment_by_student(
    user,
    api_client,
) -> None:
    """Test comment creation by student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    course.students.add(user)
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    comment = factories.CommentFactory.build()
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy("api:comment-list"),
        data={
            "content": comment.content,
            "task": task.id,
            "parent": "",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert models.Comment.objects.filter(
        content=comment.content,
        task=task.id,
        user=user.id,
        parent=None,
    ).exists()


def test_create_comment_by_not_student(
    user,
    api_client,
) -> None:
    """Test comment creation by not student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    comment = factories.CommentFactory.build()
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy("api:comment-list"),
        data={
            "content": comment.content,
            "task": task.id,
            "parent": "",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_owner_update_comment(
    user,
    api_client,
) -> None:
    """Test update comment by owner."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    course.students.add(user)
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    comment = factories.CommentFactory.create(
        task=task,
        user=user,
    )
    api_client.force_authenticate(user=user)
    new_name = "My comment"
    response = api_client.put(
        reverse_lazy("api:comment-detail", kwargs={"pk": comment.pk}),
        data={
            "content": new_name,
            "task": comment.task.id,
            "parent": "" if comment.parent is None else comment.parent,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert models.Comment.objects.filter(
        content=new_name,
        task=comment.task.id,
        parent=comment.parent,
        user=comment.user.id,
    ).exists()


def test_not_owner_update_comment(
    user,
    api_client,
) -> None:
    """Test update comment by another user."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    comment = factories.CommentFactory.create(
        task=task,
        user=user,
    )
    api_client.force_authenticate(user=user)
    new_name = "My comment"
    response = api_client.put(
        reverse_lazy("api:comment-detail", kwargs={"pk": comment.pk}),
        data={
            "content": new_name,
            "task": comment.task.id,
            "parent": "" if comment.parent is None else comment.parent,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_owner_remove_comment(
    user,
    api_client,
) -> None:
    """Test comment review by owner."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    course.students.add(user)
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    comment = factories.CommentFactory.create(
        task=task,
        user=user,
    )
    api_client.force_authenticate(user=user)
    api_client.delete(
        reverse_lazy("api:comment-detail", kwargs={"pk": comment.pk}),
    )
    assert comment not in models.Comment.objects.all()


def test_not_owner_remove_comment(
    user,
    api_client,
) -> None:
    """Test remove comment by another user."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    course.students.add(user)
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    comment = factories.CommentFactory.create(
        task=task,
    )
    api_client.force_authenticate(user=user)
    response = api_client.delete(
        reverse_lazy("api:comment-detail", kwargs={"pk": comment.pk}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_not_student_read_comment(
    user,
    api_client,
) -> None:
    """Test read comment by not student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    comment = factories.CommentFactory.create(
        task=task,
    )
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse_lazy("api:comment-detail", kwargs={"pk": comment.pk}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_student_read_comment(
    user,
    api_client,
) -> None:
    """Test read comment by not student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    course.students.add(user)
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    comment = factories.CommentFactory.create(
        task=task,
    )
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse_lazy("api:comment-detail", kwargs={"pk": comment.pk}),
    )
    assert response.status_code == status.HTTP_200_OK


def test_not_auth_read_comment(
    api_client,
) -> None:
    """Test read comment by not auth user."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    comment = factories.CommentFactory.create(
        task=task,
    )
    response = api_client.get(
        reverse_lazy("api:comment-detail", kwargs={"pk": comment.pk}),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_owner_course_read_comment(
    user,
    api_client,
) -> None:
    """Test read comment by owner of course."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    comment = factories.CommentFactory.create(
        task=task,
    )
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse_lazy("api:comment-detail", kwargs={"pk": comment.pk}),
    )
    assert response.status_code == status.HTTP_200_OK
