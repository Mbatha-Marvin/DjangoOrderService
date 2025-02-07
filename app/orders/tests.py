import uuid
import httpx
import environ
from django.test import TestCase

from rest_framework.test import APIClient
from .models import Order
from customers.models import Customer
from .services.order_service import OrderService

# Load environment variables
env = environ.Env()
environ.Env.read_env()
AT_TEST_PHONENUMBER = env("AT_TEST_PHONENUMBER", default="+254700000000")
CLIENT_ID = env("CLIENT_ID")
CLIENT_SECRET = env("CLIENT_SECRET")
OPENID_TOKEN_ENDPOINT = env("OPENID_TOKEN_ENDPOINT")


class OrderAPITestCase(TestCase):
    """Test suite for the Orders API."""

    def setUp(self) -> None:
        """Set up test data and API client."""
        self.client = APIClient()
        self.customer = Customer.objects.create(
            id=uuid.uuid4(),
            name="Jane Doe",
            email="janedoe@example.com",
            phone_number=AT_TEST_PHONENUMBER,
            address="456 Test Avenue",
        )
        self.order = Order.objects.create(
            id=uuid.uuid4(),
            customer=self.customer,
            item_name="Laptop",
            quantity=1,
            amount="1500.00",
            status="Pending",
        )
        access_token = self.get_access_token()
        if access_token is None:
            raise Exception("Can Not get Access Token")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def get_access_token(self) -> str | None:
        """
        Fetches an OpenID access token using client credentials.
        Returns:
            str: The access token.
        """
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials",
        }
        try:
            response = httpx.post(OPENID_TOKEN_ENDPOINT, data=data, timeout=10.0)
            response.raise_for_status()
            return response.json()["access_token"]
        except httpx.HTTPStatusError as e:
            print(f"Error: Unable to fetch token - {e.response.text}")
            return None
        except httpx.RequestError:
            print(f"Error: OpenID server unreachable.\n{OPENID_TOKEN_ENDPOINT = }")
            return None

    def test_create_order(self) -> None:
        """Ensure we can create a new order."""
        data = {
            "customer": str(self.customer.id),
            "item_name": "Phone",
            "quantity": 2,
            "amount": "1000.00",
            "status": "Pending",
        }
        response = self.client.post("/api/orders/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["item_name"], "Phone")

    def test_get_orders(self) -> None:
        """Ensure we can retrieve a list of orders."""
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_update_order(self) -> None:
        """Ensure we can update an existing order."""
        data = {"status": "Completed"}
        response = self.client.patch(
            f"/api/orders/{self.order.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "Completed")

    def test_delete_order(self) -> None:
        """Ensure we can delete an order."""
        response = self.client.delete(f"/api/orders/{self.order.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_authentication_required(self) -> None:
        """Ensure authentication is required for API access."""
        self.client.credentials()  # Clear credentials
        response = self.client.get("/api/orders/")
        print(f"{response.content = }")
        print(f"{response.status_code = }")
        self.assertEqual(response.status_code, 403)


class OrderModelTestCase(TestCase):
    """Test suite for the Order model."""

    def test_order_creation(self) -> None:
        """Ensure order instances are created correctly."""
        customer = Customer.objects.create(
            name="Alice Johnson",
            email="alice@example.com",
            phone_number=AT_TEST_PHONENUMBER,
            address="789 Test Road",
        )
        order = Order.objects.create(
            customer=customer,
            item_name="Book",
            quantity=3,
            amount="50.00",
            status="Pending",
        )
        self.assertEqual(order.item_name, "Book")
        self.assertEqual(order.quantity, 3)


class OrderServiceTestCase(TestCase):
    """Test suite for the Order service layer."""

    def test_create_order(self) -> None:
        """Ensure the OrderService creates orders correctly."""
        customer = Customer.objects.create(
            name="Bob Brown",
            email="bob@example.com",
            phone_number=AT_TEST_PHONENUMBER,
            address="789 Another Road",
        )
        data = {
            "customer": customer,
            "item_name": "Headphones",
            "quantity": 1,
            "amount": "100.00",
            "status": "Pending",
        }
        order = OrderService.create_order(data)
        self.assertEqual(order.item_name, "Headphones")
        self.assertEqual(order.customer, customer)

    def test_update_order(self) -> None:
        """Ensure the OrderService updates orders correctly."""
        customer = Customer.objects.create(
            name="Charlie Green",
            email="charlie@example.com",
            phone_number=AT_TEST_PHONENUMBER,
            address="123 Old Street",
        )
        order = Order.objects.create(
            customer=customer,
            item_name="Keyboard",
            quantity=1,
            amount="100.00",
            status="Pending",
        )
        data = {"status": "Completed"}
        updated_order = OrderService.update_order(order, data)
        self.assertEqual(updated_order.status, "Completed")

    def test_delete_order(self) -> None:
        """Ensure the OrderService deletes orders correctly."""
        customer = Customer.objects.create(
            name="David White",
            email="david@example.com",
            phone_number=AT_TEST_PHONENUMBER,
            address="456 New Street",
        )
        order = Order.objects.create(
            customer=customer,
            item_name="Mouse",
            quantity=1,
            amount="50.00",
            status="Pending",
        )
        OrderService.delete_order(order)
        self.assertFalse(Order.objects.filter(id=order.id).exists())
