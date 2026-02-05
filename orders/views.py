from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from stores.models import Store
from .serializers import OrderCreateSerializer, OrderSerializer
from .services import create_order


from django.db.models import Count
from rest_framework import generics
from .models import Order
from .serializers import OrderListSerializer



# Create your views here.

class OrderCreateView(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        store = Store.objects.get(id=serializer.validated_data["store_id"])
        items = serializer.validated_data["items"]

        order = create_order(store, items)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)



class StoreOrderListView(generics.ListAPIView):
    serializer_class = OrderListSerializer

    def get_queryset(self):
        store_id = self.kwargs["store_id"]

        return (
            Order.objects
            .filter(store_id=store_id)
            .annotate(total_items=Count("items"))
            .order_by("-created_at")
        )
