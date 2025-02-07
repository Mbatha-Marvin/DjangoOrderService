from core.utils import send_sms
from orders.models import Order
from customers.models import Customer


class OrderService:
    """
    Handles business logic related to orders.
    """

    @staticmethod
    def create_order(data: dict) -> Order:
        """
        Creates a new order and sends an SMS confirmation.

        Args:
            data (dict): Order details.

        Returns:
            Order: The newly created order instance.
        """
        order = Order.objects.create(**data)
        print(f"Placed {data = }")
        print(f"{order = }")
        OrderService._send_order_notification(order, "placed")
        return order

    @staticmethod
    def update_order(order: Order, data: dict) -> Order:
        """
        Updates an existing order and sends an SMS notification.

        Args:
            order (Order): The order instance.
            data (dict): Updated order data.

        Returns:
            Order: The updated order instance.p
        """
        for key, value in data.items():
            setattr(order, key, value)
        order.save()
        OrderService._send_order_notification(order, "updated")
        return order

    @staticmethod
    def delete_order(order: Order) -> None:
        """
        Deletes an order and sends an SMS cancellation notice.

        Args:
            order (Order): The order instance.
        """
        OrderService._send_order_notification(order, "cancelled")
        order.delete()

    @staticmethod
    def _send_order_notification(order: Order, action: str) -> None:
        """
        Sends an SMS notification about an order action.

        Args:
            order (Order): The order instance.
            action (str): The action performed (placed, updated, cancelled).
        """
        messages = {
            "placed": f"Your order for {order.item_name} has been placed.",
            "updated": f"Your order for {order.item_name} has been updated. Status: {order.status}.",
            "cancelled": f"Your order for {order.item_name} has been cancelled.",
        }

        customer: Customer = order.customer
        if customer.phone_number:
            response = send_sms(customer.phone_number, messages[action])

            return response
        return None
