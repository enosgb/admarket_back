import pytest
from django.urls import reverse
from rest_framework import status

from ads.models import Store


@pytest.mark.django_db
class TestStoreAPI:
    def test_list_stores_admin(self, admin_client, admin_user):
        Store.objects.create(name="Loja 1", active=True, city="SP", state="SP")
        Store.objects.create(name="Loja 2", active=False, city="RJ", state="RJ")

        url = reverse("ads_stores_list")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        assert "results" in response.data

    def test_list_stores_user_read_only(self, user_client, user):
        Store.objects.create(name="Loja 1", active=True)
        url = reverse("ads_stores_list")
        response = user_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_filter_by_active(self, admin_client):
        Store.objects.create(name="Loja Ativa", active=True)
        Store.objects.create(name="Loja Inativa", active=False)

        url = reverse("ads_stores_list") + "?active=True"
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert all(store["active"] for store in response.data["results"])
        assert len(response.data["results"]) == 1

    def test_search_by_name(self, admin_client):
        Store.objects.create(name="Loja A")
        Store.objects.create(name="Loja B")

        url = reverse("ads_stores_list")
        response = admin_client.get(url, {"search": "Loja A"}, format="json")

        assert response.status_code == 200
        results = [r for r in response.data["results"] if r["name"] == "Loja A"]
        assert len(results) == 1

    def test_ordering_by_created_at(self, admin_client):
        Store.objects.create(name="Loja A")
        Store.objects.create(name="Loja B")
        url = reverse("ads_stores_list") + "?ordering=-created_at"
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["name"] == "Loja B"

    def test_create_store_admin(self, admin_client, mock_cloudinary):
        payload = {
            "name": "Nova Loja",
            "active": True,
            "city": "SP",
            "state": "SP",
            "description": "Descrição da loja",
        }
        url = reverse("ads_stores_list")
        response = admin_client.post(url, payload, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert Store.objects.filter(name="Nova Loja").exists()

    def test_create_store_user_forbidden(self, user_client):
        payload = {"name": "Loja Proibida"}
        url = reverse("ads_stores_list")
        response = user_client.post(url, payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_store(self, admin_client):
        store = Store.objects.create(name="Loja Teste")
        url = reverse("ads_stores_retrieve_update_destroy", args=[store.id])
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == store.name

    def test_update_store_admin(self, admin_client):
        store = Store.objects.create(name="Loja Antiga")
        url = reverse("ads_stores_retrieve_update_destroy", args=[store.id])
        payload = {"name": "Loja Atualizada"}
        response = admin_client.patch(url, payload, format="multipart")
        assert response.status_code == status.HTTP_200_OK
        store.refresh_from_db()
        assert store.name == "Loja Atualizada"

    def test_update_store_user_forbidden(self, user_client):
        store = Store.objects.create(name="Loja Antiga")
        url = reverse("ads_stores_retrieve_update_destroy", args=[store.id])
        payload = {"name": "Loja Atualizada"}
        response = user_client.patch(url, payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_store_admin(self, admin_client):
        store = Store.objects.create(name="Loja Teste")
        url = reverse("ads_stores_retrieve_update_destroy", args=[store.id])
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Store.objects.filter(id=store.id).exists()

    def test_delete_store_user_forbidden(self, user_client):
        store = Store.objects.create(name="Loja Teste")
        url = reverse("ads_stores_retrieve_update_destroy", args=[store.id])
        response = user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
