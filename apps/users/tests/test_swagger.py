import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_swagger_accessible_by_admin(admin_client):
    url = reverse("api-docs")
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_swagger_ui_not_accessible_by_normal_user(user, auth_client):
    url = reverse("api-docs")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_api_schema_generated_successfully(admin_client):
    url = reverse("api-schema")
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
