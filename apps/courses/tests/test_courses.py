import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.courses import factories, models

pytestmark = pytest.mark.django_db


def test_create_course(
    user,
    api_client,
) -> None:
    """Test course creation."""
    category = factories.CategoryFactory.create()
    course = factories.CourseFactory.build(
        category=category,
        owner=user,
    )
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy("api:course-list"),
        data={
            "name": course.name,
            "description": course.description,
            "image": course.image,
            "price": course.price,
            "category": category.id,
            "status": course.status,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert models.Course.objects.filter(
        name=course.name,
        description=course.description,
        price=course.price,
        owner=user.id,
        category=category.id,
        status=course.status,
    ).exists()


def test_owner_update_course(
    user,
    api_client,
) -> None:
    """Test update course by owner."""
    category = factories.CategoryFactory.create()
    course = factories.CourseFactory.create(
        owner=user,
        category=category,
    )
    new_name = "My course"
    api_client.force_authenticate(user=user)
    response = api_client.put(
        reverse_lazy(
            "api:course-detail",
            kwargs={"pk": course.pk},
        ),
        data={
            "name": new_name,
            "description": course.description,
            "price": course.price,
            "category": category.id,
            "status": course.status,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert models.Course.objects.filter(
        name=new_name,
        description=course.description,
        price=course.price,
        owner=user.id,
        category=category.id,
        status=course.status,
    ).exists()


def test_not_owner_update_course(
    user,
    api_client,
) -> None:
    """Test update course by another user."""
    category = factories.CategoryFactory.create()
    course = factories.CourseFactory.create(
        category=category,
    )
    api_client.force_authenticate(user=user)
    new_name = "My course"
    response = api_client.put(
        reverse_lazy(
            "api:course-detail",
            kwargs={"pk": course.pk},
        ),
        data={
            "name": new_name,
            "description": course.description,
            "price": course.price,
            "category": category.id,
            "status": course.status,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_owner_remove_course(
    user,
    api_client,
) -> None:
    """Test remove course by owner."""
    course = factories.CourseFactory.create(
        owner=user,
    )
    api_client.force_authenticate(user=user)
    api_client.delete(
        reverse_lazy(
            "api:course-detail",
            kwargs={"pk": course.pk},
        ),
    )
    assert course not in models.Course.objects.all()


def test_not_owner_remove_course(
    user,
    api_client,
) -> None:
    """Test remove course by another user."""
    course = factories.CourseFactory.create()
    api_client.force_authenticate(user=user)
    response = api_client.delete(
        reverse_lazy(
            "api:course-detail",
            kwargs={"pk": course.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_add_and_remove_student(
    user,
    api_client,
) -> None:
    """Test add and remove student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    api_client.force_authenticate(user=user)
    api_client.post(
        reverse_lazy(
            "courses:add-students",
            kwargs={"pk": course.pk},
        )
    )
    assert user in course.students.all()
    api_client.post(
        reverse_lazy(
            "courses:add-students",
            kwargs={"pk": course.pk},
        )
    )
    assert user not in course.students.all()


def test_add_and_remove_interest(
    user,
    api_client,
) -> None:
    """Success test add and remove interest."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    api_client.force_authenticate(user=user)
    course.students.add(user)
    api_client.post(
        reverse_lazy(
            "courses:add-interest",
            kwargs={"pk": course.pk},
        )
    )
    assert user in course.interest_users.all()
    api_client.post(
        reverse_lazy(
            "courses:add-interest",
            kwargs={"pk": course.pk},
        )
    )
    assert user not in course.interest_users.all()


def test_add_and_remove_wanted_passing_success(
    user,
    api_client,
) -> None:
    """Success test add and remove wanted passing."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    api_client.force_authenticate(user=user)
    course.students.add(user)
    api_client.post(
        reverse_lazy(
            "courses:add-wanted-passing",
            kwargs={"pk": course.pk},
        )
    )
    assert user in course.want_pass_users.all()
    api_client.post(
        reverse_lazy(
            "courses:add-wanted-passing",
            kwargs={"pk": course.pk},
        )
    )
    assert user not in course.want_pass_users.all()


def test_add_and_remove_wanted_passing_failed(
    user,
    api_client,
) -> None:
    """Failed test add and remove wanted passing."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy(
            "courses:add-wanted-passing",
            kwargs={"pk": course.pk},
        )
    )
    assert user not in course.want_pass_users.all()
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_add_and_remove_achive_success(
    user,
    api_client,
) -> None:
    """Success test add and remove achive."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    api_client.force_authenticate(user=user)
    course.students.add(user)
    api_client.post(
        reverse_lazy(
            "courses:add-achive",
            kwargs={"pk": course.pk},
        )
    )
    assert user in course.archive_users.all()
    api_client.post(
        reverse_lazy(
            "courses:add-achive",
            kwargs={"pk": course.pk},
        )
    )
    assert user not in course.archive_users.all()


def test_add_and_remove_achive_failed(
    user,
    api_client,
) -> None:
    """Failed test add and remove achive."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy(
            "courses:add-achive",
            kwargs={"pk": course.pk},
        )
    )
    assert user not in course.archive_users.all()
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_not_student_read_course(
    user,
    api_client,
) -> None:
    """Test read course by not student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse_lazy(
            "api:course-detail",
            kwargs={"pk": course.pk},
        )
    )
    assert response.status_code == status.HTTP_200_OK


def test_student_read_course(
    user,
    api_client,
) -> None:
    """Test read course by student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    course.students.add(user)
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse_lazy(
            "api:course-detail",
            kwargs={"pk": course.pk},
        )
    )
    assert response.status_code == status.HTTP_200_OK


def test_not_auth_read_course(
    api_client,
) -> None:
    """Test read course by not auth."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    response = api_client.get(
        reverse_lazy(
            "api:course-detail",
            kwargs={"pk": course.pk},
        )
    )
    assert response.status_code == status.HTTP_200_OK


def test_owner_read_course(
    user,
    api_client,
) -> None:
    """Test read course by owner."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
        owner=user,
    )
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse_lazy(
            "api:course-detail",
            kwargs={"pk": course.pk},
        )
    )
    assert response.status_code == status.HTTP_200_OK
