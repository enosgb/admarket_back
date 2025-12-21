import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

from ads.models import Product, ProductImage, Category


@pytest.fixture
def category(db):
    return Category.objects.create(name="Eletrônicos")


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name="Notebook",
        description="Produto teste",
        active=True,
        category=category,
    )


@pytest.fixture
def product_payload(category):
    return {
        "name": "Mouse",
        "description": "Mouse gamer",
        "active": True,
        "category": category.id,
    }


@pytest.fixture
def image_file():
    file = io.BytesIO()
    image = Image.new("RGB", (100, 100), color="red")
    image.save(file, "JPEG")
    file.seek(0)

    return SimpleUploadedFile(
        "test.jpg",
        file.read(),
        content_type="image/jpeg",
    )


@pytest.mark.django_db
class TestProductModel:
    def test_create_product(self, category):
        product = Product.objects.create(
            name="Teclado",
            category=category,
        )

        assert product.id is not None
        assert product.active is True
        assert product.category == category

    def test_str_representation(self, product):
        assert str(product) == "Notebook"


@pytest.mark.django_db
class TestProductImageModel:
    def test_create_main_image(self, product, image_file):
        image = ProductImage.objects.create(
            product=product,
            image=image_file,
            is_main=True,
        )

        assert image.id is not None
        assert image.is_main is True

    def test_only_one_main_image_allowed(self, product, image_file):
        ProductImage.objects.create(
            product=product,
            image=image_file,
            is_main=True,
        )

        with pytest.raises(Exception):
            ProductImage.objects.create(
                product=product,
                image=image_file,
                is_main=True,
            )


@pytest.mark.django_db
class TestProductListCreateAPI:
    def test_list_products_as_admin(self, admin_client, product):
        url = reverse("product_list_create")
        response = admin_client.get(url)

        assert response.status_code == 200
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == product.name

    def test_list_products_as_user(self, user_client, product):
        url = reverse("product_list_create")
        response = user_client.get(url)

        assert response.status_code == 200

    def test_list_products_without_auth_returns_401(self, api_client):
        url = reverse("product_list_create")
        response = api_client.get(url)

        assert response.status_code == 401

    def test_create_product_as_admin(self, admin_client, product_payload):
        url = reverse("product_list_create")
        response = admin_client.post(url, product_payload)

        assert response.status_code == 201
        assert Product.objects.count() == 1

    def test_create_product_as_non_admin_returns_403(
        self, user_client, product_payload
    ):
        url = reverse("product_list_create")
        response = user_client.post(url, product_payload)

        assert response.status_code == 403

    def test_filter_product_by_category(self, admin_client, category, product):
        url = reverse("product_list_create") + f"?category={category.id}"
        response = admin_client.get(url)

        assert response.status_code == 200
        assert response.data["count"] == 1

    def test_search_product_by_name(self, admin_client, product):
        url = reverse("product_list_create") + "?search=Notebook"
        response = admin_client.get(url)

        assert response.status_code == 200
        assert response.data["count"] == 1


@pytest.mark.django_db
class TestProductRetrieveUpdateDestroyAPI:
    def test_retrieve_product_as_admin(self, admin_client, product):
        url = reverse("product_detail", kwargs={"pk": product.id})
        response = admin_client.get(url)

        assert response.status_code == 200
        assert response.data["name"] == product.name

    def test_retrieve_product_as_user(self, user_client, product):
        url = reverse("product_detail", kwargs={"pk": product.id})
        response = user_client.get(url)

        assert response.status_code == 200

    def test_retrieve_product_without_auth_returns_401(self, api_client, product):
        url = reverse("product_detail", kwargs={"pk": product.id})
        response = api_client.get(url)

        assert response.status_code == 401

    def test_update_product_as_admin(self, admin_client, product):
        url = reverse("product_detail", kwargs={"pk": product.id})
        response = admin_client.put(
            url,
            {
                "name": "Notebook Pro",
                "description": "Atualizado",
                "active": False,
                "category": product.category.id,
            },
        )

        assert response.status_code == 200
        product.refresh_from_db()
        assert product.name == "Notebook Pro"

    def test_update_product_as_non_admin_returns_403(self, user_client, product):
        url = reverse("product_detail", kwargs={"pk": product.id})
        response = user_client.put(
            url,
            {
                "name": "Tentativa",
                "category": product.category.id,
            },
        )

        assert response.status_code == 403

    def test_delete_product_as_admin(self, admin_client, product):
        url = reverse("product_detail", kwargs={"pk": product.id})
        response = admin_client.delete(url)

        assert response.status_code == 204
        assert Product.objects.count() == 0

    def test_delete_product_as_non_admin_returns_403(self, user_client, product):
        url = reverse("product_detail", kwargs={"pk": product.id})
        response = user_client.delete(url)

        assert response.status_code == 403


@pytest.mark.django_db
class TestProductImageAPI:
    def test_create_main_image_as_admin(self, admin_client, product, image_file):
        url = reverse(
            "product_image_create",
            kwargs={"product_id": product.id},
        )

        response = admin_client.post(
            url,
            {"image": image_file, "is_main": True},
            format="multipart",
        )

        assert response.status_code == 201
        assert ProductImage.objects.count() == 1

    def test_create_second_main_image_returns_400(
        self, admin_client, product, image_file
    ):
        ProductImage.objects.create(
            product=product,
            image=image_file,
            is_main=True,
        )

        url = reverse(
            "product_image_create",
            kwargs={"product_id": product.id},
        )

        response = admin_client.post(
            url,
            {"image": image_file, "is_main": True},
            format="multipart",
        )

        assert response.status_code == 400
        assert "is_main" in response.data

    def test_create_image_as_non_admin_returns_403(
        self, user_client, product, image_file
    ):
        url = reverse(
            "product_image_create",
            kwargs={"product_id": product.id},
        )

        response = user_client.post(
            url,
            {"image": image_file},
            format="multipart",
        )

        assert response.status_code == 403

    def test_delete_image_as_admin(self, admin_client, product, image_file):
        image = ProductImage.objects.create(
            product=product,
            image=image_file,
        )

        url = reverse(
            "product_image_update-delete",
            kwargs={"id": image.id},
        )

        response = admin_client.delete(url)

        assert response.status_code == 204
        assert ProductImage.objects.count() == 0
