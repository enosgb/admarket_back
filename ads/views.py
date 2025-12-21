from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from .models import Category, Product, ProductImage
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    ProductCreateUpdateSerializer,
    ProductDetailSerializer,
    ProductImageCreateSerializer,
    ProductListSerializer,
)
from .swagger_schemas import (
    products_images_create_schema,
    products_images_update_schema,
)


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

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["active", "category"]
    search_fields = ["id", "name", "active", "category__name"]

    orderning_filters = ["id", "name", "category__name", "created_at"]
    orderning = ["name"]

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
