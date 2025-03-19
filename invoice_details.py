import streamlit as st
import requests
import pandas as pd
from api_calls import(
    fetch_invoice_details, authorize
)

def download_document(file_url):
    pass

@st.dialog("Detailed view of the selected item")
def display_details(file_id):
    invoice_details = fetch_invoice_details(file_id).json()

    st.write("## Invoice Details")
    st.write(f"**Invoice Number:** {invoice_details.get('id')}")
    st.write(f"**Invoice Date:** {invoice_details.get('service_period')}")
    st.write(f"**Debitor:** {invoice_details.get('Debitor', {}).get('name')}")
    st.write(f"**Service Period:** {invoice_details.get('service_period')}")
    st.write(f"**Due Date:** {invoice_details.get('due_date')}")

    st.write("### Items")
    items_data = [
        {
            "Description": item.get("description"),
            "Amount": item.get("amount"),
            "Price": item.get("price"),
            "VAT Rate": item.get("vat_rate")
        }
        for item in invoice_details.get("items", [])
    ]
    
    if items_data:
        df_items = pd.DataFrame(items_data)
        st.dataframe(df_items)

    st.write(f"**Total Netto:** {invoice_details.get('netto')}")
    st.write(f"**Total Brutto:** {invoice_details.get('brutto')}")
    st.write(f"**Open Amount (Balance):** {invoice_details.get('balance')}")
    st.write(f"**Total VAT:** {invoice_details.get('total_vat')}")

    file_url = invoice_details.get("file", {}).get("file_url")
    filename = invoice_details.get("file", {}).get("download_filename", "invoice.pdf")

    if file_url:
        auth_response = authorize()

        if auth_response.status_code == 200:
            access_token = auth_response.json().get("access_token")

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            download_response = requests.get(file_url, headers=headers)

            if download_response.status_code == 200:
                    # Automatically trigger download when the invoice is selected
                    st.download_button(
                        label="📥 Click to Download Invoice",
                        data=download_response.content,
                        file_name=filename,
                        mime="application/pdf"
                    )
            else:
                st.error(" Failed to fetch the invoice file.")
        else:
            st.warning("Could not authenticate request.")
    else:
        st.warning("No invoice file available.")