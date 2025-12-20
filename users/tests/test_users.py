# users/tests/test_users.py
import pytest
from rest_framework import status

from users.models import User


@pytest.mark.django_db
class TestUserAPI:

    def test_list_users_admin(self, admin_client, sample_users):
        """Admins podem listar todos os usuários"""
        response = admin_client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == len(sample_users) + 1

    def test_list_users_non_admin_forbidden(self, authenticated_client, sample_users):
        """Usuários normais não podem listar todos"""
        response = authenticated_client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_search_no_results(self, admin_client):
        response = admin_client.get("/api/v1/users/?search=nonexistent")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    def test_search_by_name(self, admin_client, sample_users):
        response = admin_client.get("/api/v1/users/?search=Ana")
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Ana Silva"

    def test_search_by_email(self, admin_client, sample_users):
        response = admin_client.get("/api/v1/users/?search=bruno")
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["email"] == "bruno@example.com"

    def test_ordering_by_name(self, admin_client, sample_users):
        response = admin_client.get("/api/v1/users/?ordering=name")
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    def test_create_user_admin(self, admin_client, mock_image):
        data = {
            "email": "novo@test.com",
            "password": "senha123",
            "name": "Novo Usuário",
        }
        response = admin_client.post("/api/v1/users/", data)
        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email="novo@test.com")
        assert user.name == "Novo Usuário"

    def test_create_user_non_admin_forbidden(self, authenticated_client):
        data = {"email": "novo2@test.com", "password": "123", "name": "User 2"}
        response = authenticated_client.post("/api/v1/users/", data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_self_user(self, authenticated_client, sample_users):
        user = sample_users[0]
        response = authenticated_client.get(f"/api/v1/users/{user.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email

    def test_retrieve_other_user_forbidden(self, authenticated_client, sample_users):
        user = sample_users[1]
        response = authenticated_client.get(f"/api/v1/users/{user.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_partial_update_self(self, authenticated_client, sample_users):
        user = sample_users[0]
        data = {"name": "Atualizado"}
        response = authenticated_client.patch(f"/api/v1/users/{user.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Atualizado"

    def test_partial_update_other_user_forbidden(
        self, authenticated_client, sample_users
    ):
        user = sample_users[1]
        data = {"name": "Tentativa"}
        response = authenticated_client.patch(f"/api/v1/users/{user.id}/", data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_user_admin(self, admin_client, sample_users):
        user = sample_users[0]
        response = admin_client.delete(f"/api/v1/users/{user.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(id=user.id).exists()

    def test_delete_user_non_admin_forbidden(self, authenticated_client, sample_users):
        user = sample_users[0]
        response = authenticated_client.delete(f"/api/v1/users/{user.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_access(self, api_client, sample_users):
        response = api_client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        data = {"email": "teste@test.com", "password": "123"}
        response = api_client.post("/api/v1/users/", data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user = sample_users[0]
        response = api_client.get(f"/api/v1/users/{user.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pagination_page_2(self, admin_client):
        for i in range(15):
            User.objects.create_user(
                email=f"user{i}@test.com", password="123", name=f"User {i}"
            )
        response = admin_client.get("/api/v1/users/?page=2")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 2
        assert len(response.data["results"]) <= 10
