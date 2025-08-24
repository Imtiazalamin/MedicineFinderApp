import django_filters
from .models import stock

class StockFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')  # >=
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')  # <=

    class Meta:
        model = stock
        fields = ['pharmacy', 'medicine_name']
