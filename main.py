import requests
from constants import (
    USERNAME, PASSWORD, CLIENT_ID, CLIENT_SECRET, GRANT_TYPE, AUTH_URL, INVOICE_URL
)

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

# Step 1: Get the access token
#auth_response = requests.post(auth_url, json=auth_payload)
auth_response = requests.post(auth_url, data=auth_payload)

if auth_response.status_code == 200:
    access_token = auth_response.json().get("access_token")
    print("Access Token:", access_token)

    # Step 2: Use the token to make an API request
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    invoice_response = requests.get(invoice_url, headers=headers)

    if invoice_response.status_code == 200:
        print("Invoice List:", invoice_response.json())
    else:
        print("Failed to fetch invoices:", invoice_response.status_code, invoice_response.text)
else:
    print("Authentication failed:", auth_response.status_code, auth_response.text)
    print("Response Status Code:", auth_response.status_code)
    print("Response JSON:", auth_response.json())  # This will show the error message
    print("Response Headers:", auth_response.headers)

