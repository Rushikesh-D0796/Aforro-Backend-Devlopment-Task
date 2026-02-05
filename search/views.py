from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Prefetch

from products.models import Product
from products.serializers import ProductSerializer, ProductSearchSerializer
from stores.models import Inventory

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from products.models import Product

# Create your views here.

class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        qs = Product.objects.select_related("category")

        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            )

        if store_id := self.request.GET.get("store_id"):
            qs = qs.prefetch_related(
                Prefetch(
                    "inventory_set",
                    queryset=Inventory.objects.filter(store_id=store_id)
                )
            )

        return qs.order_by("-created_at")

    serializer_class = ProductSearchSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        qs = Product.objects.select_related("category")

        q = self.request.GET.get("q")
        category = self.request.GET.get("category")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        store_id = self.request.GET.get("store_id")
        in_stock = self.request.GET.get("in_stock")
        sort = self.request.GET.get("sort")

        # Keyword search
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            )

        # Filters
        if category:
            qs = qs.filter(category__name__iexact=category)

        if min_price:
            qs = qs.filter(price__gte=min_price)

        if max_price:
            qs = qs.filter(price__lte=max_price)

        # Inventory filter
        if store_id:
            inv_qs = Inventory.objects.filter(store_id=store_id)
            qs = qs.prefetch_related(Prefetch("inventory_set", queryset=inv_qs))

            if in_stock == "true":
                qs = qs.filter(inventory__store_id=store_id, inventory__quantity__gt=0)

        # Sorting
        if sort == "price":
            qs = qs.order_by("price")
        elif sort == "newest":
            qs = qs.order_by("-created_at")

        return qs
    
class ProductSuggestView(APIView):
    def get(self, request):
        query = request.GET.get("q", "").strip()

        if len(query) < 3:
            return Response({"error": "Minimum 3 characters required"}, status=400)

        # Prefix matches
        prefix_matches = Product.objects.filter(title__istartswith=query).values_list("title", flat=True)[:10]

        # Other matches (avoid duplicates)
        remaining = 10 - len(prefix_matches)
        other_matches = Product.objects.filter(
            Q(title__icontains=query) & ~Q(title__istartswith=query)
        ).values_list("title", flat=True)[:remaining]

        suggestions = list(prefix_matches) + list(other_matches)

        return Response({"suggestions": suggestions})