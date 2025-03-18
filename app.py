import streamlit as st
import json
import pandas as pd
from api_calls import (
    fetch_invoices
)

st.set_page_config(
    page_title="Frontend Cracks",
    page_icon="🧠",
    layout="wide"
)

st.title("Frontend Cracks")
st.write("A coding challenge from the Brayn.io")

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

st.title("Invoice List")
st.dataframe(df)