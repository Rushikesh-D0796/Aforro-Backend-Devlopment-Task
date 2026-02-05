from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListAPIView
from .models import Inventory
from .serializers import InventorySerializer

# Create your views here.


@method_decorator(cache_page(60 * 5), name="dispatch")  # cache for 5 mins
class StoreInventoryView(ListAPIView):
    serializer_class = InventorySerializer

    def get_queryset(self):
        store_id = self.kwargs["store_id"]

        return (
            Inventory.objects
            .filter(store_id=store_id)
            .select_related("product__category")
            .order_by("product__title")
        )
