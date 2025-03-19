import requests
from constants import (
    USERNAME, PASSWORD, CLIENT_ID, CLIENT_SECRET, GRANT_TYPE, AUTH_URL, INVOICE_URL
)

def authorize():
    # Authentication credentials
    credentials = {
        "username": USERNAME,
        "password": PASSWORD,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": GRANT_TYPE
    }
    url = AUTH_URL

    auth_response = requests.post(url, data=credentials)

    return auth_response

def fetch_invoices(): 
    invoice_url = INVOICE_URL
    
    auth_response = authorize()

    if auth_response.status_code == 200:
        access_token = auth_response.json().get("access_token")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        invoice_response = requests.get(invoice_url, headers=headers)

        if invoice_response.status_code == 200:
            return invoice_response
        else:
            print("Failed to fetch invoices:", invoice_response.status_code, invoice_response.text)
    else:
        print("Authentication failed:", auth_response.status_code, auth_response.text)
        print("Response Status Code:", auth_response.status_code)
        print("Response JSON:", auth_response.json())  
        print("Response Headers:", auth_response.headers)

def fetch_invoice_details(id):
    invoice_url = INVOICE_URL + f"/{id}"
    
    auth_response = authorize()

    if auth_response.status_code == 200:
        access_token = auth_response.json().get("access_token")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        invoice_response = requests.get(invoice_url, headers=headers)

        if invoice_response.status_code == 200:
            return invoice_response
        else:
            print("Failed to fetch invoice:", invoice_response.status_code, invoice_response.text)
    else:
        print("Authentication failed:", auth_response.status_code, auth_response.text)
        print("Response Status Code:", auth_response.status_code)
        print("Response JSON:", auth_response.json())  
        print("Response Headers:", auth_response.headers)

if __name__ == "__main__":
    details = fetch_invoice_details("3085")