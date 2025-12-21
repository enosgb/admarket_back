from django.urls import path

from .views import (
    AdCreateAndListView,
    AdRetrieveUpdateDestroyView,
    CategoryListAndCreateView,
    CategoryRetrieveUpdateDestroyView,
    FavoriteDeleteView,
    FavoriteListCreateView,
    ProductImageCreateView,
    ProductImageRetrieveUpdateDestroyView,
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    StoreCreateAndListView,
    StoreRetrieveUpdateDestroyView,
)

urlpatterns = [
    path(
        "categories/", CategoryListAndCreateView.as_view(), name="ads_categories_list"
    ),
    path(
        "categories/<int:id>",
        CategoryRetrieveUpdateDestroyView.as_view(),
        name="ads_categories_retrieve_update_destroy",
    ),
    path(
        "products/",
        ProductListCreateView.as_view(),
        name="product_list_create",
    ),
    path(
        "products/<int:pk>/",
        ProductRetrieveUpdateDestroyView.as_view(),
        name="product_detail",
    ),
    path(
        "products/<int:product_id>/images/",
        ProductImageCreateView.as_view(),
        name="product_image_create",
    ),
    path(
        "products/images/<int:id>/",
        ProductImageRetrieveUpdateDestroyView.as_view(),
        name="product_image_update-delete",
    ),
    path("stores/", StoreCreateAndListView.as_view(), name="ads_stores_list"),
    path(
        "stores/<int:id>/",
        StoreRetrieveUpdateDestroyView.as_view(),
        name="ads_stores_retrieve_update_destroy",
    ),
    path("", AdCreateAndListView.as_view(), name="ads_list"),
    path(
        "<int:id>/",
        AdRetrieveUpdateDestroyView.as_view(),
        name="ads_retrieve_update_destroy",
    ),
    path("favorites/", FavoriteListCreateView.as_view(), name="favorites_list_create"),
    path(
        "favorites/<int:favorite_id>/",
        FavoriteDeleteView.as_view(),
        name="favorite_delete",
    ),
]
