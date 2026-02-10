import os
import requests
from requests.auth import HTTPBasicAuth

PAYD_BASE_URL = os.getenv("PAYD_BASE_URL")
PAYD_USERNAME = os.getenv("PAYD_API_USERNAME")
PAYD_PASSWORD = os.getenv("PAYD_API_PASSWORD")


class PaydPaymentService:
    @staticmethod
    def initiate_payment(amount, phone_number, narration, callback_url, transaction_ref):
        url = f"{PAYD_BASE_URL}/payments"

        payload = {
            "username": PAYD_USERNAME,
            "channel": "MPESA",
            "amount": amount,
            "phone_number": phone_number,
            "narration": narration,
            "currency": "KES",
            "callback_url": callback_url,
            "reference": transaction_ref
        }

        try:
            response = requests.post(url, json=payload,
                                     auth=HTTPBasicAuth(PAYD_USERNAME, PAYD_PASSWORD))
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
