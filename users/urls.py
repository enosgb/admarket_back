from django.urls import path

from .views import UserListAndCreateView, UserRetrieveUpdateDestroyView

urlpatterns = [
    path("", UserListAndCreateView.as_view(), name="user_list_create"),
    path(
        "<int:id>/",
        UserRetrieveUpdateDestroyView.as_view(),
        name="user_retrieve_update_destroy",
    ),
]
