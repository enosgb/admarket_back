import pytest
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from users.models import User
from users.serializers import UserSerializer
from rest_framework import status


@pytest.mark.django_db
class TestLoginView:
    def test_login_success(self, api_client, user):
        url = reverse("login")
        data = {"email": user.email, "password": "strongpassword123"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "Login realizado"
        assert response.data["user"]["email"] == user.email

    def test_login_invalid_credentials(self, api_client, user):
        url = reverse("login")
        data = {"email": user.email, "password": "wrongpassword"}
        response = api_client.post(url, data)
        assert response.status_code == 401
        assert response.data["detail"] == "Credenciais inválidas"


@pytest.mark.django_db
class TestLogoutView:
    def test_logout_authenticated(self, authenticated_client):
        url = reverse("logout")
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "Logout realizado"

    def test_logout_unauthenticated(self, api_client):
        url = reverse("logout")
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestResetPassword:
    def test_reset_password_request_existing_email(self, api_client, user, mocker):
        url = reverse("reset_password")
        mock_send = mocker.patch("utils.send_email.SendEmail.send", return_value=True)

        response = api_client.post(url, {"email": user.email})
        assert response.status_code == 200
        assert "instruções" in response.data["detail"]
        mock_send.assert_called_once()

    def test_reset_password_request_nonexistent_email(self, api_client, mocker):
        url = reverse("reset_password")
        mock_send = mocker.patch("utils.send_email.SendEmail.send", return_value=True)

        response = api_client.post(url, {"email": "fake@example.com"})
        assert response.status_code == 200
        assert "instruções" in response.data["detail"]
        mock_send.assert_not_called()

    def test_reset_password_confirm_success(self, api_client, user):
        url = reverse("reset_password_confirm")
        token = default_token_generator.make_token(user)
        data = {"email": user.email, "token": token, "new_password": "newpass123"}
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert response.data["detail"] == "Senha alterada com sucesso."
        user.refresh_from_db()
        assert user.check_password("newpass123")

    def test_reset_password_confirm_invalid_token(self, api_client, user):
        url = reverse("reset_password_confirm")
        data = {
            "email": user.email,
            "token": "invalidtoken",
            "new_password": "newpass123",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400
        assert "Token inválido" in response.data["detail"]


@pytest.mark.django_db
class TestChangePassword:
    def test_change_password_success(self, authenticated_client, user):
        url = reverse("change_password")
        data = {
            "old_password": "strongpassword123",
            "new_password": "newpass123",
            "confirm_new_password": "newpass123",
        }
        response = authenticated_client.put(url, data)
        assert response.status_code == 200
        assert response.data["detail"] == "Senha alterada com sucesso."
        user.refresh_from_db()
        assert user.check_password("newpass123")

    def test_change_password_wrong_old(self, authenticated_client):
        url = reverse("change_password")
        data = {
            "old_password": "wrongold",
            "new_password": "newpass123",
            "confirm_new_password": "newpass123",
        }
        response = authenticated_client.put(url, data)
        assert response.status_code == 400
        assert "Senha antiga está incorreta." in str(response.data)

    def test_change_password_mismatch_new(self, authenticated_client):
        url = reverse("change_password")
        data = {
            "old_password": "strongpassword123",
            "new_password": "newpass123",
            "confirm_new_password": "different",
        }
        response = authenticated_client.put(url, data)
        assert response.status_code == 400
        assert "As novas senhas não coincidem." in str(response.data)
