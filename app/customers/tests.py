import uuid
import httpx
import environ
from django.test import TestCase

from rest_framework.test import APIClient
from .models import Customer
from .services.customer_service import CustomerService

# Load environment variables
env = environ.Env()
environ.Env.read_env()
AT_TEST_PHONENUMBER = env("AT_TEST_PHONENUMBER", default="+254700000000")
CLIENT_ID = env("CLIENT_ID")
CLIENT_SECRET = env("CLIENT_SECRET")
OPENID_TOKEN_ENDPOINT = env("OPENID_TOKEN_ENDPOINT")


class CustomerAPITestCase(TestCase):
    """Test suite for the Customers API."""

    def setUp(self) -> None:
        """Set up test data and API client."""
        self.client = APIClient()
        self.customer = Customer.objects.create(
            id=uuid.uuid4(),
            name="John Doe",
            email="johndoe@example.com",
            phone_number=AT_TEST_PHONENUMBER,
            address="123 Test Street",
        )
        access_token = self.get_access_token()
        if access_token is httpx.RequestError or access_token is httpx.HTTPStatusError:
            raise Exception(
                f"Can Not get Access Token \n{OPENID_TOKEN_ENDPOINT = } \n {access_token.response.text}"
            )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def get_access_token(self) -> str | httpx.HTTPStatusError | httpx.RequestError:
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
            # response.raise_for_status()
            print(f"{OPENID_TOKEN_ENDPOINT = }\n{CLIENT_SECRET = } {CLIENT_ID = }\n{response.text = }")
            return response.json()["access_token"]
        except httpx.HTTPStatusError as e:
            print(f"Error: Unable to fetch token - {e.response.text}")
            return e
        except httpx.RequestError as e:
            print(f"Error: OpenID server unreachable.\n{OPENID_TOKEN_ENDPOINT = }")
            return e

    def test_create_customer(self) -> None:
        """Ensure we can create a new customer."""
        data = {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "phone_number": AT_TEST_PHONENUMBER,
            "address": "789 Test Road",
        }
        response = self.client.post("/api/customers/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Alice Johnson")

    def test_get_customers(self) -> None:
        """Ensure we can retrieve a list of customers."""
        response = self.client.get("/api/customers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_update_customer(self) -> None:
        """Ensure we can update an existing customer."""
        data = {"name": "John Smith", "address": "Updated Address"}
        response = self.client.patch(
            f"/api/customers/{self.customer.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "John Smith")

    def test_delete_customer(self) -> None:
        """Ensure we can delete a customer."""
        response = self.client.delete(f"/api/customers/{self.customer.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Customer.objects.filter(id=self.customer.id).exists())

    def test_authentication_required(self) -> None:
        """Ensure authentication is required for API access."""
        self.client.credentials()  # Clear credentials
        response = self.client.get("/api/customers/")
        self.assertEqual(response.status_code, 403)


class CustomerModelTestCase(TestCase):
    """Test suite for the Customer model."""

    def test_customer_creation(self) -> None:
        """Ensure customer instances are created correctly."""
        customer = Customer.objects.create(
            name="Jane Doe",
            email="janedoe@example.com",
            phone_number=AT_TEST_PHONENUMBER,
            address="456 Test Avenue",
        )
        self.assertEqual(customer.name, "Jane Doe")
        self.assertEqual(customer.email, "janedoe@example.com")


class CustomerServiceTestCase(TestCase):
    """Test suite for the Customer service layer."""

    def test_create_customer(self) -> None:
        """Ensure the CustomerService creates customers correctly."""
        data = {
            "name": "Bob Brown",
            "email": "bob@example.com",
            "phone_number": AT_TEST_PHONENUMBER,
            "address": "789 Another Road",
        }
        customer = CustomerService.create_customer(data)
        self.assertEqual(customer.name, "Bob Brown")
        self.assertEqual(customer.email, "bob@example.com")

    def test_update_customer(self) -> None:
        """Ensure the CustomerService updates customers correctly."""
        customer = Customer.objects.create(
            name="Charlie Green",
            email="charlie@example.com",
            phone_number=AT_TEST_PHONENUMBER,
            address="123 Old Street",
        )
        data = {"name": "Charlie Blue", "address": "Updated Address"}
        updated_customer = CustomerService.update_customer(customer, data)
        self.assertEqual(updated_customer.name, "Charlie Blue")
        self.assertEqual(updated_customer.address, "Updated Address")
