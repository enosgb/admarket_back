import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from ads.models import (
    Ad,
    Category,
    Product,
    Store,
)


@pytest.mark.django_db
class TestAdAPI:

    @pytest.fixture
    def category(self):
        return Category.objects.create(name="Eletrônicos", active=True)

    @pytest.fixture
    def store(self):
        return Store.objects.create(name="Loja Teste")

    @pytest.fixture
    def product(self, category):
        return Product.objects.create(name="Produto Teste", category=category)

    @pytest.fixture
    def ad_factory(self, store, product):
        def create_ad(**kwargs):
            return Ad.objects.create(store=store, product=product, **kwargs)

        return create_ad

    def test_list_ads_admin(self, admin_client, ad_factory):
        ad_factory(title="Ad 1", active=True)
        ad_factory(title="Ad 2", active=False)

        url = reverse("ads_list")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        assert "results" in response.data

    def test_list_ads_user_read_only(self, user_client, ad_factory):
        ad_factory(title="Ad 1")
        url = reverse("ads_list")
        response = user_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_filter_by_active_and_published(self, admin_client, ad_factory):
        ad_factory(title="Ativo e publicado", active=True, published=True)
        ad_factory(title="Inativo ou não publicado", active=False, published=True)

        url = reverse("ads_list")
        response = admin_client.get(url, {"active": True, "published": True})
        results = response.data["results"]
        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert all(ad["active"] and ad["published"] for ad in results)

    def test_search_by_title_description(self, admin_client, ad_factory):
        ad_factory(title="Super Oferta", description="Descrição 123")
        ad_factory(title="Outra Coisa", description="Descrição aleatória")

        url = reverse("ads_list")
        response = admin_client.get(url, {"search": "Super Oferta"})
        results = [
            ad for ad in response.data["results"] if ad["title"] == "Super Oferta"
        ]
        assert response.status_code == 200
        assert len(results) == 1

    def test_ordering_by_created_at(self, admin_client, ad_factory):
        ad1 = ad_factory(title="Ad 1")
        ad2 = ad_factory(title="Ad 2")

        url = reverse("ads_list")
        response = admin_client.get(url, {"ordering": "-created_at"})
        assert response.status_code == 200
        assert response.data["results"][0]["title"] == ad2.title

    def test_create_ad_admin(self, admin_client, store, product):
        payload = {
            "title": "Nova Oferta",
            "description": "Descrição da nova oferta",
            "store": store.id,
            "product": product.id,
            "active": True,
            "published": True,
        }
        url = reverse("ads_list")
        response = admin_client.post(url, payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert Ad.objects.filter(title="Nova Oferta").exists()

    def test_create_ad_user_forbidden(self, user_client, store, product):
        payload = {"title": "Oferta Proibida", "store": store.id, "product": product.id}
        url = reverse("ads_list")
        response = user_client.post(url, payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_ad(self, admin_client, ad_factory):
        ad = ad_factory(title="Ad Teste")
        url = reverse("ads_retrieve_update_destroy", args=[ad.id])
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == ad.title

    def test_update_ad_admin(self, admin_client, ad_factory):
        ad = ad_factory(title="Ad Antigo")
        payload = {"title": "Ad Atualizado"}
        url = reverse("ads_retrieve_update_destroy", args=[ad.id])
        response = admin_client.patch(url, payload)
        ad.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert ad.title == "Ad Atualizado"

    def test_update_ad_user_forbidden(self, user_client, ad_factory):
        ad = ad_factory(title="Ad Antigo")
        payload = {"title": "Ad Atualizado"}
        url = reverse("ads_retrieve_update_destroy", args=[ad.id])
        response = user_client.patch(url, payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_ad_admin(self, admin_client, ad_factory):
        ad = ad_factory(title="Ad Teste")
        url = reverse("ads_retrieve_update_destroy", args=[ad.id])
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Ad.objects.filter(id=ad.id).exists()

    def test_delete_ad_user_forbidden(self, user_client, ad_factory):
        ad = ad_factory(title="Ad Teste")
        url = reverse("ads_retrieve_update_destroy", args=[ad.id])
        response = user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_filter_by_store_and_product(self, admin_client, category):
        store1 = Store.objects.create(name="Loja 1")
        store2 = Store.objects.create(name="Loja 2")
        product1 = Product.objects.create(name="Produto 1", category=category)
        product2 = Product.objects.create(name="Produto 2", category=category)

        ad1 = Ad.objects.create(title="Ad 1", store=store1, product=product1)
        ad2 = Ad.objects.create(title="Ad 2", store=store2, product=product2)

        url = reverse("ads_list")
        response = admin_client.get(url, {"store": store1.id, "product": product1.id})
        results = response.data["results"]
        assert len(results) == 1
        assert results[0]["title"] == ad1.title

    def test_filter_by_start_and_end_date(self, admin_client, ad_factory):
        now = timezone.now()
        ad1 = ad_factory(title="Ad Hoje", start_date=now)
        ad2 = ad_factory(title="Ad Amanhã", start_date=now + timezone.timedelta(days=1))

        url = reverse("ads_list")
        response = admin_client.get(url, {"start_date": now.isoformat()})
        results = response.data["results"]
        assert len(results) >= 1
        assert any(ad["title"] == "Ad Hoje" for ad in results)
