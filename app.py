import streamlit as st
import pandas as pd
from api_calls import(
    fetch_invoices, fetch_invoice_details
) 
from invoice_details import display_details

st.set_page_config(
    page_title="Frontend Cracks",
    page_icon="🧠",
    layout="wide"
)

st.title("Frontend Cracks")
st.write("A coding challenge from Brayn.io")

data = fetch_invoices().json()
invoices = data['_embedded']['list_debits']

invoice_list = []
for invoice in invoices:
    invoice_data = {
        'Invoice Number': invoice.get('id'),
        'Invoice Date': invoice.get('service_period'),
        'Net Amount (Netto)': invoice.get('netto'),
        'Gross Amount (Brutto)': invoice.get('brutto'),
        'Open Amount (Balance)': invoice.get('balance'),
        'Debitor': invoice.get('Debitor', {}).get('name')
    }
    invoice_list.append(invoice_data)

df = pd.DataFrame(invoice_list)

df.insert(0, "Select", False)

edited_df = st.data_editor(df, key="invoice_table", use_container_width=True, num_rows="fixed")

selected_invoice = edited_df.loc[edited_df["Select"] == True, "Invoice Number"]

if not selected_invoice.empty:
    # Get selected invoice ID
    invoice_id = selected_invoice.values[0]  

    display_details(invoice_id)
