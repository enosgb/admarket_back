from django.urls import path

from .views import (
    CategoryListAndCreateView,
    CategoryRetrieveUpdateDestroyView,
    ProductImageCreateView,
    ProductImageRetrieveUpdateDestroyView,
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
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
]
