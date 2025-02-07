from customers.models import Customer


class CustomerService:
    """
    Handles business logic related to customers.
    """

    @staticmethod
    def create_customer(data: dict) -> Customer:
        """
        Creates a new customer.

        Args:
            data (dict): Customer details.

        Returns:
            Customer: The newly created customer instance.
        """
        return Customer.objects.create(**data)

    @staticmethod
    def update_customer(customer: Customer, data: dict) -> Customer:
        """
        Updates an existing customer.

        Args:
            customer (Customer): The customer instance.
            data (dict): Updated customer data.

        Returns:
            Customer: The updated customer instance.
        """
        for key, value in data.items():
            setattr(customer, key, value)
        customer.save()
        return customer

    @staticmethod
    def delete_customer(customer: Customer) -> None:
        """
        Deletes a customer.

        Args:
            customer (Customer): The customer instance.
        """
        customer.delete()
