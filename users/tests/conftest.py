# conftest.py
import pytest
from rest_framework.test import APIClient
from users.models import User
from unittest.mock import patch

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_users(db):
    """Usuários de exemplo"""
    users = [
        User.objects.create_user(email="ana@example.com", password="123", name="Ana Silva"),
        User.objects.create_user(email="bruno@example.com", password="123", name="Bruno Lima"),
        User.objects.create_user(email="carlos@example.com", password="123", name="Carlos Souza"),
    ]
    return users

@pytest.fixture
def authenticated_client(db, sample_users):
    """Cliente autenticado com o primeiro usuário da lista"""
    user = sample_users[0]
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def admin_client(db):
    """Cliente autenticado como superuser"""
    admin = User.objects.create_superuser(
        email="admin@test.com",
        password="admin123",
        name="Admin Test"
    )
    client = APIClient()
    client.force_authenticate(user=admin)
    return client

@pytest.fixture
def mock_image():
    """Mock para campo ImageField evitando upload real"""
    with patch("users.models.MediaCloudinaryStorage.save") as mock_save:
        mock_save.return_value = "mocked_image.jpg"
        yield mock_save
