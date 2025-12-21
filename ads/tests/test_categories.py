import pytest
from django.urls import reverse

from ads.models import Category


@pytest.mark.django_db
class TestCategoryModel:
    def test_create_category(self):
        category = Category.objects.create(
            name="Automóveis",
            description="Categoria de carros",
            active=True,
        )

        assert category.id is not None
        assert category.name == "Automóveis"
        assert category.active is True

    def test_str_representation(self):
        category = Category.objects.create(name="Moda")
        assert str(category) == "Moda"


@pytest.mark.django_db
class TestCategoryListCreateAPI:
    def test_list_categories_as_admin(self, admin_client):
        Category.objects.create(name="Casa")
        Category.objects.create(name="Tecnologia")

        url = reverse("ads_categories_list")
        response = admin_client.get(url)

        assert response.status_code == 200
        assert response.data["count"] == 2
        assert response.data["current_page"] == 1
        assert len(response.data["results"]) == 2

    def test_list_categories_without_auth_returns_401(self, api_client):
        url = reverse("ads_categories_list")
        response = api_client.get(url)

        assert response.status_code == 401

    def test_create_category_as_admin(self, admin_client, category_payload):
        url = reverse("ads_categories_list")

        response = admin_client.post(
            url,
            category_payload,
            format="multipart",
        )

        assert response.status_code == 201
        assert response.data["name"] == category_payload["name"]
        assert Category.objects.count() == 1

    def test_create_category_as_non_admin_returns_403(
        self, user_client, category_payload
    ):
        url = reverse("ads_categories_list")

        response = user_client.post(
            url,
            category_payload,
            format="multipart",
        )

        assert response.status_code == 403

    def test_create_category_without_name_returns_400(self, admin_client):
        url = reverse("ads_categories_list")

        response = admin_client.post(
            url,
            {"description": "Sem nome"},
            format="multipart",
        )

        assert response.status_code == 400
        assert "name" in response.data

    def test_search_category_by_name(self, admin_client):
        Category.objects.create(name="Eletrônicos")
        Category.objects.create(name="Roupas")

        url = reverse("ads_categories_list") + "?search=Eletrônicos"
        response = admin_client.get(url)

        assert response.status_code == 200
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == "Eletrônicos"


@pytest.mark.django_db
class TestCategoryRetrieveUpdateDestroyAPI:
    def test_retrieve_category_as_admin(self, admin_client):
        category = Category.objects.create(name="Games")

        url = reverse(
            "ads_categories_retrieve_update_destroy",
            kwargs={"id": category.id},
        )

        response = admin_client.get(url)

        assert response.status_code == 200
        assert response.data["name"] == "Games"

    def test_retrieve_category_without_auth_returns_401(self, api_client):
        category = Category.objects.create(name="Público")

        url = reverse(
            "ads_categories_retrieve_update_destroy",
            kwargs={"id": category.id},
        )

        response = api_client.get(url)

        assert response.status_code == 401

    def test_update_category_put_as_admin(self, admin_client):
        category = Category.objects.create(name="Antigo")

        url = reverse(
            "ads_categories_retrieve_update_destroy",
            kwargs={"id": category.id},
        )

        payload = {
            "name": "Atualizado",
            "description": "Nova descrição",
            "active": False,
        }

        response = admin_client.put(url, payload, format="multipart")

        assert response.status_code == 200
        category.refresh_from_db()
        assert category.name == "Atualizado"
        assert category.active is False

    def test_update_category_put_as_non_admin_returns_403(self, user_client):
        category = Category.objects.create(name="Protegido")

        url = reverse(
            "ads_categories_retrieve_update_destroy",
            kwargs={"id": category.id},
        )

        response = user_client.put(
            url,
            {"name": "Tentativa"},
            format="multipart",
        )

        assert response.status_code == 403

    def test_partial_update_category_patch_as_admin(self, admin_client):
        category = Category.objects.create(name="Parcial")

        url = reverse(
            "ads_categories_retrieve_update_destroy",
            kwargs={"id": category.id},
        )

        response = admin_client.patch(
            url,
            {"name": "Parcial Atualizado"},
            format="multipart",
        )

        assert response.status_code == 200
        category.refresh_from_db()
        assert category.name == "Parcial Atualizado"

    def test_delete_category_as_admin(self, admin_client):
        category = Category.objects.create(name="Excluir")

        url = reverse(
            "ads_categories_retrieve_update_destroy",
            kwargs={"id": category.id},
        )

        response = admin_client.delete(url)

        assert response.status_code == 204
        assert Category.objects.count() == 0

    def test_delete_category_as_non_admin_returns_403(self, user_client):
        category = Category.objects.create(name="Protegido")

        url = reverse(
            "ads_categories_retrieve_update_destroy",
            kwargs={"id": category.id},
        )

        response = user_client.delete(url)

        assert response.status_code == 403

    def test_retrieve_nonexistent_category_returns_404(self, admin_client):
        url = reverse(
            "ads_categories_retrieve_update_destroy",
            kwargs={"id": 999},
        )

        response = admin_client.get(url)

        assert response.status_code == 404
