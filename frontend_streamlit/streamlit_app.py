import streamlit as st
import requests
import os

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Loan Payment Portal", layout="centered")
st.title("Loan Payment Portal")

st.sidebar.header("Config")
api_override = st.sidebar.text_input("API URL", API_URL)
if api_override:
    API_URL = api_override

st.header("Customers")
if st.button("Refresh customers"):
    st.experimental_rerun()

try:
    resp = requests.get(f"{API_URL}/customers", timeout=5)
    if resp.status_code == 200:
        customers = resp.json()
    else:
        customers = []
        st.warning(f"Unable to load customers: HTTP {resp.status_code}")
except Exception as e:
    customers = []
    st.warning(f"Error loading customers: {e}")

for c in customers:
    st.subheader(f"{c.get('name')} — {c.get('account_number')}")
    st.write(f"Outstanding: {c.get('outstanding_amount', 'N/A')}")

st.header("Make EMI Payment")
with st.form("pay_form"):
    account = st.text_input("Account number")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Pay EMI")

if submitted:
    if not account:
        st.error("Account number is required")
    elif amount <= 0:
        st.error("Amount must be > 0")
    else:
        try:
            r = requests.post(f"{API_URL}/payments", json={"account_number": account, "amount": amount}, timeout=5)
            if r.status_code == 200:
                st.success("Payment successful")
            else:
                try:
                    st.error(r.json())
                except Exception:
                    st.error(f"Payment failed: status {r.status_code}")
        except Exception as exc:
            st.error(f"Request failed: {exc}")

st.markdown("---")
st.caption("This Streamlit UI interacts with the FastAPI backend.")
