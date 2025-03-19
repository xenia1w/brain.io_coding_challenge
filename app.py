import streamlit as st
import pandas as pd
from api_calls import fetch_invoices, fetch_invoice_details

st.set_page_config(
    page_title="Frontend Cracks",
    page_icon="🧠",
    layout="wide"
)

st.title("Frontend Cracks")
st.write("A coding challenge from Brayn.io")

# Fetch invoice data
data = fetch_invoices().json()
invoices = data['_embedded']['list_debits']

# Process data into DataFrame
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

# Add a selection column
df.insert(0, "Select", False)

# Use st.data_editor for an interactive experience
edited_df = st.data_editor(df, key="invoice_table", use_container_width=True, num_rows="fixed")

# Get the selected invoice (first selected row)
selected_invoice = edited_df.loc[edited_df["Select"] == True, "Invoice Number"]

# Show details when an invoice is selected
if not selected_invoice.empty:
    invoice_id = selected_invoice.values[0]  # Get the first selected invoice ID
    invoice_details = fetch_invoice_details(invoice_id).json()

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
