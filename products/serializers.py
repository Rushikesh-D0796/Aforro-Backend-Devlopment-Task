from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "category"]





class ProductSearchSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    inventory_quantity = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "category", "inventory_quantity"]
