import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        email="admin@test.com",
        password="admin123",
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def category_payload():
    return {
        "name": "Eletrônicos",
        "description": "Categoria de eletrônicos",
        "active": True,
    }


@pytest.fixture(autouse=True)
def mock_cloudinary(mocker):
    """
    Evita upload real no Cloudinary em TODOS os testes
    """
    mocker.patch(
        "cloudinary_storage.storage.MediaCloudinaryStorage._save",
        return_value="fake_image.jpg",
    )
