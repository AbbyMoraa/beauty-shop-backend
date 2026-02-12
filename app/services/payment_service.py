import os
import requests
from requests.auth import HTTPBasicAuth

class PaydPaymentService:
    @staticmethod
    def initiate_payment(amount, phone_number, narration, callback_url, transaction_ref):
        url = f"{os.getenv('PAYD_BASE_URL')}/payments"
        username = os.getenv('PAYD_API_USERNAME')
        password = os.getenv('PAYD_API_PASSWORD')

        payload = {
            "username": username,
            "channel": "MPESA",
            "amount": amount,
            "phone_number": phone_number,
            "narration": narration,
            "currency": "KES",
            "callback_url": callback_url,
            "reference": transaction_ref
        }

        try:
            resp = requests.post(url, json=payload, auth=HTTPBasicAuth(username, password))
            return resp.json(), resp.status_code
        except Exception as e:
            return {"error": str(e)}, 500
