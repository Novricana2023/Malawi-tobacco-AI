import streamlit as st

st.set_page_config(layout="wide")

st.title("🌿 Tobacco Leaf Disease Assistant 🌿")
st.write("Welcome to your AI-powered agricultural advisory system!")
st.write("Please navigate using the sidebar to access different features like disease checking, soil analysis, and market data.")

# You might add some introductory content or direct links to pages here
# For example, a simple button to navigate to the disease checker:
# if st.button("Go to Disease Checker"): 
#     st.query_params["page"] = "2_disease_checker"

# Note: Streamlit multi-page apps automatically use files in the 'pages' directory.
# The file names (e.g., '1_my_field.py') determine the order and name in the sidebar.

