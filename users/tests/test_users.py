# test_users.py
import pytest
from rest_framework import status
from users.models import User

@pytest.mark.django_db
class TestUserAPI:

    def test_list_users_authenticated(self, authenticated_client, sample_users):
        response = authenticated_client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) == len(sample_users)

    def test_search_no_results(self, authenticated_client):
        response = authenticated_client.get("/api/v1/users/?search=nonexistent")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    def test_search_by_name(self, authenticated_client, sample_users):
        response = authenticated_client.get("/api/v1/users/?search=Ana")
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Ana Silva"

    def test_search_by_email(self, authenticated_client, sample_users):
        response = authenticated_client.get("/api/v1/users/?search=bruno")
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["email"] == "bruno@example.com"

    def test_ordering_by_name(self, authenticated_client, sample_users):
        response = authenticated_client.get("/api/v1/users/?ordering=name")
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    def test_ordering_invalid_field(self, authenticated_client):
        response = authenticated_client.get("/api/v1/users/?ordering=invalid")
        # DRF normalmente ignora campos inválidos e retorna ordenação padrão
        assert response.status_code == status.HTTP_200_OK

    def test_create_user(self, authenticated_client, mock_image):
        data = {
            "email": "novo@test.com",
            "password": "senha123",
            "name": "Novo Usuário",
            "image": "dummy.jpg"
        }
        response = authenticated_client.post("/api/v1/users/", data)
        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email="novo@test.com")
        assert user.name == "Novo Usuário"
        assert user.image.name == "mocked_image.jpg"

    def test_create_user_invalid_email(self, authenticated_client):
        data = {"email": "", "password": "123"}
        response = authenticated_client.post("/api/v1/users/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_user(self, authenticated_client, sample_users):
        user = sample_users[0]
        response = authenticated_client.get(f"/api/v1/users/{user.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email

    def test_partial_update_user(self, authenticated_client, sample_users):
        user = sample_users[0]
        data = {"name": "Ana Atualizada"}
        response = authenticated_client.patch(f"/api/v1/users/{user.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Ana Atualizada"

    def test_update_user_unauthorized(self, api_client, sample_users):
        user = sample_users[0]
        response = api_client.patch(f"/api/v1/users/{user.id}/", {"name": "X"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_user(self, admin_client, sample_users):
        user = sample_users[0]
        response = admin_client.delete(f"/api/v1/users/{user.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(id=user.id).exists()

    def test_delete_user_unauthorized(self, authenticated_client, sample_users):
        user = sample_users[0]
        response = authenticated_client.delete(f"/api/v1/users/{user.id}/")
        # Usuário normal não pode deletar
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_access_list(self, api_client):
        response = api_client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unauthenticated_cannot_create(self, api_client):
        data = {"email": "teste@test.com", "password": "123"}
        response = api_client.post("/api/v1/users/", data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pagination_page_2(self, authenticated_client):
        # Cria 15 usuários extras para testar a paginação
        for i in range(15):
            User.objects.create_user(
                email=f"user{i}@test.com", password="123", name=f"User {i}"
            )
        response = authenticated_client.get("/api/v1/users/?page=2")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 2
        assert len(response.data["results"]) <= 10
