from django.urls import path

from .views import CategoryListAndCreateView, CategoryRetrieveUpdateDestroyView

urlpatterns = [
    path("categories/", CategoryListAndCreateView.as_view(), name="ads_categories_list"),
    path(
        "categories/<int:id>",
        CategoryRetrieveUpdateDestroyView.as_view(),
        name="ads_categories_retrieve_update_destroy",
    ),
]
