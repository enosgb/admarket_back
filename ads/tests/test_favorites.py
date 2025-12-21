import pytest
from django.urls import reverse

from ads.models import Category, Favorite, Product


@pytest.fixture
def category(db, category_payload):
    return Category.objects.create(**category_payload)


@pytest.fixture
def products(db, category):
    p1 = Product.objects.create(
        name="Produto A", category=category, stock=10, sale_price=100
    )
    p2 = Product.objects.create(
        name="Produto B", category=category, stock=5, sale_price=50
    )
    p3 = Product.objects.create(
        name="Produto C", category=category, stock=0, sale_price=200
    )
    return [p1, p2, p3]


@pytest.fixture
def favorites(db, user, products):
    fav1 = Favorite.objects.create(user=user, product=products[0])
    fav2 = Favorite.objects.create(user=user, product=products[1])
    return [fav1, fav2]


@pytest.mark.django_db
def test_list_favorites(user_client, favorites):
    url = reverse("favorites_list_create")
    response = user_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert data["count"] == 2
    product_names = [item["product"]["name"] for item in data["results"]]
    assert "Produto A" in product_names
    assert "Produto B" in product_names


@pytest.mark.django_db
def test_list_favorites_requires_auth(api_client):
    url = reverse("favorites_list_create")
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_favorite(user_client, products):
    url = reverse("favorites_list_create")
    payload = {"product_id": products[2].id}

    response = user_client.post(url, payload)
    assert response.status_code == 201
    data = response.json()
    assert data["product"]["id"] == products[2].id
    assert Favorite.objects.filter(
        user__email="user@test.com", product=products[2]
    ).exists()


@pytest.mark.django_db
def test_create_duplicate_favorite(user_client, favorites):
    url = reverse("favorites_list_create")
    payload = {"product_id": favorites[0].product.id}

    response = user_client.post(url, payload)
    assert response.status_code in [201, 201]
    assert (
        Favorite.objects.filter(
            user=favorites[0].user, product=favorites[0].product
        ).count()
        == 1
    )


@pytest.mark.django_db
def test_delete_favorite(user_client, favorites):
    fav = favorites[0]
    url = reverse("favorite_delete", kwargs={"favorite_id": fav.id})

    response = user_client.delete(url)
    assert response.status_code == 204
    assert not Favorite.objects.filter(id=fav.id).exists()


@pytest.mark.django_db
def test_delete_favorite_not_owned(user_client, products, db):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    other_user = User.objects.create_user(email="other@test.com", password="123456")
    fav = Favorite.objects.create(user=other_user, product=products[0])

    url = reverse("favorite_delete", kwargs={"favorite_id": fav.id})
    response = user_client.delete(url)
    assert response.status_code == 404
    assert Favorite.objects.filter(id=fav.id).exists()


@pytest.mark.django_db
def test_delete_favorite_requires_auth(api_client, favorites):
    fav = favorites[0]
    url = reverse("favorite_delete", kwargs={"favorite_id": fav.id})
    response = api_client.delete(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_search_favorites(user_client, favorites):
    url = reverse("favorites_list_create") + "?search=Produto A"
    response = user_client.get(url)
    data = response.json()
    assert data["count"] == 1
    assert data["results"][0]["product"]["name"] == "Produto A"


@pytest.mark.django_db
def test_filter_favorites_by_product(user_client, favorites):
    url = reverse("favorites_list_create") + f"?product={favorites[0].product.id}"
    response = user_client.get(url)
    data = response.json()
    assert data["count"] == 1
    assert data["results"][0]["product"]["id"] == favorites[0].product.id


@pytest.mark.django_db
def test_order_favorites(user_client, favorites):
    url = reverse("favorites_list_create") + "?ordering=product__name"
    response = user_client.get(url)
    data = response.json()
    names = [item["product"]["name"] for item in data["results"]]
    assert names == sorted(names)
