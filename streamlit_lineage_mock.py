
pip install streamlit pyvis pandas
import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components
import pandas as pd
import tempfile
import os

# Dummy retail and econ column lists
retail_cols = ['Order ID', 'Date', 'Status', 'Qty', 'Amount', 'Customer_ID']
econ_cols = ['Transaction_ID', 'Customer_ID', 'Income', 'Gender', 'Classification']

# Dummy table data
orders_df = pd.DataFrame({
    "Order ID": [1, 2],
    "Customer_ID": [101, 102],
    "Amount": [99.99, 149.99],
    "Classification": ["Gold", "Silver"],
    "Status": ["Shipped", "Pending"]
})

# Create UI
st.title("Test: Interactive Column Lineage")

table_options = {"Orders": orders_df}

st.subheader("Interactive Column Lineage Graph")

selected_lineage_table_key = st.selectbox("Select Table for Lineage", list(table_options.keys()), key="lineage_table_select")
selected_lineage_table_df = table_options[selected_lineage_table_key]
selected_table_cols = selected_lineage_table_df.columns.tolist()

net = Network(height="700px", width="100%", directed=True)
net.barnes_hut()

# Add source + table nodes
retail_node = "Retail Data"
econ_node = "Econ Data"
rls_node = "RLS Policies"
table_node = selected_lineage_table_key

net.add_node(retail_node, label=retail_node, color='orange')
net.add_node(econ_node, label=econ_node, color='green')
net.add_node(rls_node, label=rls_node, color='red')
net.add_node(table_node, label=table_node, color='lightblue', shape='box')

# Add column nodes and edges
for col in selected_table_cols:
    col_node = f"Column: {col}"
    net.add_node(col_node, label=col, shape='ellipse')

    if col.lower() == 'classification':
        net.add_edge(rls_node, col_node)
    if col in retail_cols:
        net.add_edge(retail_node, col_node)
    if col in econ_cols:
        net.add_edge(econ_node, col_node)

    net.add_edge(col_node, table_node)

# Render the graph
with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
    tmp_path = tmp_file.name
    net.show(tmp_path)
    components.html(open(tmp_path, 'r', encoding='utf-8').read(), height=700)
    os.unlink(tmp_path)
