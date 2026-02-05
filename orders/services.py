from django.db import transaction
from django.db.models import F
from stores.models import Inventory
from .models import Order, OrderItem


@transaction.atomic
def create_order(store, items_data):
    order = Order.objects.create(store=store)

    product_ids = [item["product_id"] for item in items_data]

    inventory_qs = (
        Inventory.objects
        .select_for_update()
        .filter(store=store, product_id__in=product_ids)
    )

    inventory_map = {inv.product_id: inv for inv in inventory_qs}

    insufficient_products = []

    # Check stock first
    for item in items_data:
        product_id = item["product_id"]
        qty = item["quantity"]

        inv = inventory_map.get(product_id)
        if not inv or inv.quantity < qty:
            insufficient_products.append(product_id)

    if insufficient_products:
        order.status = Order.REJECTED
        order.save()
        return order

    # Deduct stock
    for item in items_data:
        product_id = item["product_id"]
        qty = item["quantity"]

        inv = inventory_map[product_id]
        inv.quantity = F("quantity") - qty
        inv.save()

        OrderItem.objects.create(
            order=order,
            product_id=product_id,
            quantity_requested=qty
        )

    order.status = Order.CONFIRMED
    order.save()

    return order
