from celery import shared_task
from orders.models import Order

@shared_task
def test_task():
    print("Celery is working")


@shared_task
def send_order_confirmation(order_id):
    order = Order.objects.get(id=order_id)
    print(f"Order {order.id} processed with status {order.status}")
