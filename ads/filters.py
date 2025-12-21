import django_filters

from ads.models import Ad


class AdFilter(django_filters.FilterSet):
    product_sale_price__lte = django_filters.NumberFilter(
        field_name="product__sale_price", lookup_expr="lte"
    )
    product_sale_price__gte = django_filters.NumberFilter(
        field_name="product__sale_price", lookup_expr="gte"
    )

    class Meta:
        model = Ad
        fields = [
            "active",
            "published",
            "store",
            "product",
            "start_date",
            "end_date",
            "product_sale_price__lte",
            "product_sale_price__gte",
        ]
