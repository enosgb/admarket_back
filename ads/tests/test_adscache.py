import pytest
from django.core.cache import cache
from rest_framework import status

from ads.models import Ad, Category, Product, ProductImage


@pytest.mark.django_db
class TestAdsCacheRedis:

    @pytest.fixture
    def category(self, db):
        return Category.objects.create(
            name="Categoria Teste", description="Categoria de teste", active=True
        )

    @pytest.fixture
    def product(self, category):
        return Product.objects.create(
            name="Produto Teste",
            active=True,
            category=category,
            stock=0,
            cost_price=0,
            sale_price=0,
        )

    @pytest.fixture
    def main_image(self, product):
        return ProductImage.objects.create(
            product=product, is_main=True, image="test.jpg"
        )

    @pytest.fixture
    def ad(self, product, main_image):
        return Ad.objects.create(
            title="Ad Teste",
            description="Descrição do Ad",
            active=True,
            published=True,
            product=product,
            store=None,
        )

    @pytest.fixture
    def redis_client(self):
        from django_redis import get_redis_connection
        return get_redis_connection("default")

    def test_ad_list_cache_redis(self, api_client, ad, redis_client):
        url = "/api/v1/ads/public/"
        cache.clear()
        redis_client.flushdb()

        response1 = api_client.get(url)
        assert response1.status_code == status.HTTP_200_OK
        first_results = response1.json()["results"]

        response2 = api_client.get(url)
        assert response2.status_code == status.HTTP_200_OK
        second_results = response2.json()["results"]

        assert first_results == second_results

        ad.title = "Ad Atualizado"
        ad.save()

        response3 = api_client.get(url)
        updated_results = response3.json()["results"]

        assert updated_results[0]["title"] == "Ad Atualizado"
        assert updated_results != second_results

    def test_ad_detail_cache_redis(self, api_client, ad, redis_client):
        url = f"/api/v1/ads/public/{ad.id}/"
        cache.clear()
        redis_client.flushdb()

        response1 = api_client.get(url)
        assert response1.status_code == status.HTTP_200_OK
        first_data = response1.json()

        response2 = api_client.get(url)
        assert response2.status_code == status.HTTP_200_OK
        second_data = response2.json()

        assert first_data == second_data

        ad.description = "Descrição Atualizada"
        ad.save()

        response3 = api_client.get(url)
        updated_data = response3.json()
        assert updated_data["description"] == "Descrição Atualizada"
        assert updated_data != second_data
