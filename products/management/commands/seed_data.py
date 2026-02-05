from django.core.management.base import BaseCommand
from products.models import Product, Category


class Command(BaseCommand):
    help = "Seed initial product data"

    def handle(self, *args, **kwargs):
        # Create category first
        category, _ = Category.objects.get_or_create(
            name="General"
        )

        products = [
            "Apple",
            "Banana",
            "Milk",
            "Bread",
        ]

        for title in products:
            Product.objects.get_or_create(
                title=title,              # ✅ use loop variable
                category=category,        # ✅ REQUIRED FK
                defaults={
                    "price": 10.0,
                    "description": "",
                }
            )

        self.stdout.write(
            self.style.SUCCESS("Seed data inserted successfully")
        )
