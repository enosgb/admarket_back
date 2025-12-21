from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from ads.filters import AdFilter

from .models import Ad, Category, Product, ProductImage, Store
from .permissions import IsAdminOrReadOnly
from .serializers import (
    AdSerializer,
    CategorySerializer,
    ProductCreateUpdateSerializer,
    ProductDetailSerializer,
    ProductImageCreateSerializer,
    ProductListSerializer,
    StoreSerializer,
)
from .swagger_schemas import (
    products_images_create_schema,
    products_images_update_schema,
)


# CATEGORIES
class CategoryListAndCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = ["name", "active"]

    orderning_filters = ["id", "name", "created_at"]
    orderning = ["name"]


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "id"


class ProductListCreateView(generics.ListCreateAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["active", "category", "stock", "cost_price", "sale_price"]
    search_fields = ["id", "name", "active", "category__name"]
    ordering_fields = [
        "id",
        "name",
        "category__name",
        "created_at",
        "stock",
        "cost_price",
        "sale_price",
    ]
    ordering = ["name"]

    def get_queryset(self):
        return Product.objects.select_related("category").prefetch_related(
            Prefetch(
                "images",
                queryset=ProductImage.objects.filter(is_main=True),
                to_attr="main_image",
            )
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateUpdateSerializer
        return ProductListSerializer


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    serializer_class = ProductDetailSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    def get_queryset(self):
        return Product.objects.select_related("category").prefetch_related("images")


class ProductImageCreateView(generics.CreateAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    serializer_class = ProductImageCreateSerializer
    parser_classes = [MultiPartParser, FormParser]

    @products_images_create_schema
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["product"] = get_object_or_404(Product, id=self.kwargs["product_id"])
        return context

    def perform_create(self, serializer):
        serializer.save(product=self.get_serializer_context()["product"])


class ProductImageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageCreateSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = "id"
    parser_classes = [MultiPartParser, FormParser]

    @products_images_update_schema
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @products_images_update_schema
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


# Stores
class StoreCreateAndListView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["active"]
    search_fields = ["name", "city", "state"]
    ordering_fields = ["id", "name", "active", "city", "state", "created_at"]
    ordering = ["name"]


class StoreRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "id"


# ADS
class AdCreateAndListView(generics.ListCreateAPIView):
    serializer_class = AdSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = AdFilter
    search_fields = ["title", "description"]
    ordering_fields = [
        "id",
        "title",
        "active",
        "published",
        "store",
        "product",
        "created_at",
    ]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Ad.objects.select_related("store", "product").prefetch_related(
            "product__images"
        )


class AdRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = "id"

    def get_queryset(self):
        return Ad.objects.select_related("store", "product").all()
