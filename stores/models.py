from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.location}"


class Inventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="inventory_items")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("store", "product")

    def __str__(self):
        return f"{self.store.name} - {self.product.title}"
