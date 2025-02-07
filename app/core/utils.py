import africastalking
from django.conf import settings

# Initialize Africa's Talking SDK
africastalking.initialize(settings.AT_USERNAME, settings.AT_API_KEY)
sms: africastalking.SMSService = africastalking.SMS


def send_sms(phone_number: str, message: str) -> dict:
    """
    Sends an SMS notification to a given phone number.

    Args:
        phone_number (str): The recipient's phone number.
        message (str): The message to send.

    Returns:
        dict: Response from Africa's Talking API.
    """
    try:
        print(f"Sending SMS to {phone_number = }")
        response = sms.send(message, [phone_number])
        print(f"{response = }")
        return response
    except Exception as e:
        return {"error": str(e)}
