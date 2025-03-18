import requests
from constants import (
    USERNAME, PASSWORD, CLIENT_ID, CLIENT_SECRET, GRANT_TYPE, AUTH_URL, INVOICE_URL
)

def fetch_invoices():
    # API endpoints
    auth_url = AUTH_URL
    invoice_url = INVOICE_URL

    # Authentication credentials
    auth_payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": GRANT_TYPE
    }

    auth_response = requests.post(auth_url, data=auth_payload)

    if auth_response.status_code == 200:
        access_token = auth_response.json().get("access_token")
        print("Access Token:", access_token)

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        invoice_response = requests.get(invoice_url, headers=headers)

        if invoice_response.status_code == 200:
            #print("Invoice List:", invoice_response.json())
            return invoice_response
        else:
            print("Failed to fetch invoices:", invoice_response.status_code, invoice_response.text)
    else:
        print("Authentication failed:", auth_response.status_code, auth_response.text)
        print("Response Status Code:", auth_response.status_code)
        print("Response JSON:", auth_response.json())  
        print("Response Headers:", auth_response.headers)

