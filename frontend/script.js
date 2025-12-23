// Use environment-based API URL
const API_URL = window.API_URL || "http://localhost:8000";

async function loadCustomers() {
  try {
    const resp = await fetch(`${API_URL}/customers`);
    const customers = await resp.json();
    const container = document.getElementById("customers");
    container.innerHTML = "";

    customers.forEach(customer => {
      const div = document.createElement("div");
      div.className = "customer-card";
      div.innerHTML = `
        <p><b>Account:</b> ${customer.account_number}</p>
        <p><b>Issue Date:</b> ${customer.issue_date}</p>
        <p><b>Interest Rate:</b> ${customer.interest_rate}%</p>
        <p><b>Tenure:</b> ${customer.tenure} months</p>
        <p><b>EMI Due:</b> ₹${customer.emi_due}</p>
      `;
      container.appendChild(div);
    });
  } catch (e) {
    document.getElementById("customers").innerText = "Failed to load customers.";
  }
}

// EMI payment using JSON body and showing confirmation
async function payEmi() {
  const account = document.getElementById("account").value.trim();
  const amount = document.getElementById("amount").value.trim();
  const message = document.getElementById("message");

  if (!account || !amount) {
    message.innerText = "Please enter account number and amount.";
    return;
  }

  try {
    const resp = await fetch(`${API_URL}/payments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ account_number: account, amount: Number(amount) })
    });

    if (!resp.ok) {
      const err = await resp.text();
      message.innerText = `Payment failed: ${err}`;
      return;
    }

    const data = await resp.json();
    message.innerText = data.message || "Payment successful";
    // refresh customers (balance may have changed)
    loadCustomers();
  } catch (e) {
    message.innerText = "Payment failed (network).";
  }
}

// Attach event
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('payBtn').addEventListener('click', payEmi);
  loadCustomers();
});
