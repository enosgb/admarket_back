import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def user(db):
    """Cria um usuário padrão para os testes"""
    return User.objects.create_user(
        email="test@example.com",
        password="strongpassword123",
        username="testuser"
    )

@pytest.fixture
def api_client():
    """Retorna um client da API REST"""
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user):
    """Retorna um client autenticado"""
    api_client.force_authenticate(user=user)
    return api_client
