import sqlite3
import streamlit as st
import pandas as pd

# Initialize the database
conn = sqlite3.connect('bank.db')
c = conn.cursor()

# Create customers table
c.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        balance REAL NOT NULL
    )
''')
conn.commit()

# Function to add a new customer
def add_customer(name, balance):
    c.execute('INSERT INTO customers (name, balance) VALUES (?, ?)', (name, balance))
    conn.commit()

# Function to view all customers
def view_customers():
    c.execute('SELECT * FROM customers')
    return c.fetchall()

# Function to search for a customer by ID
def search_customer(customer_id):
    c.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    return c.fetchone()

# Function to update customer information
def update_customer(customer_id, name, balance):
    c.execute('UPDATE customers SET name = ?, balance = ? WHERE id = ?', (name, balance, customer_id))
    conn.commit()

# Function to delete a customer record
def delete_customer(customer_id):
    c.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
    conn.commit()

# Function to credit account balance
def credit_balance(customer_id, amount):
    c.execute('UPDATE customers SET balance = balance + ? WHERE id = ?', (amount, customer_id))
    conn.commit()

# Function to debit account balance
def debit_balance(customer_id, amount):
    c.execute('UPDATE customers SET balance = balance - ? WHERE id = ? AND balance >= ?', (amount, customer_id, amount))
    conn.commit()

# Streamlit frontend
def main():
    st.title("Bank Management System")

    menu = ["Add Customer", "View Customers", "Search Customer", "Update Customer", "Delete Customer", "Credit Balance", "Debit Balance", "Bank Statement"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Customer":
        st.subheader("Add Customer")
        name = st.text_input("Customer Name")
        balance = st.number_input("Initial Balance", min_value=0.0, format="%.2f")
        if st.button("Add"):
            add_customer(name, balance)
            st.success(f"Customer {name} added with balance {balance}")

    elif choice == "View Customers":
        st.subheader("View Customers")
        customers = view_customers()
        df = pd.DataFrame(customers, columns=["ID", "Name", "Balance"])
        st.dataframe(df.style.set_properties(**{'background-color': 'lightblue', 'color': 'black'}))

    elif choice == "Search Customer":
        st.subheader("Search Customer")
        customer_id = st.number_input("Customer ID", min_value=1, step=1)
        if st.button("Search"):
            customer = search_customer(customer_id)
            if customer:
                st.write(f"ID: {customer[0]}, Name: {customer[1]}, Balance: {customer[2]}")
            else:
                st.error("Customer not found")

    elif choice == "Update Customer":
        st.subheader("Update Customer")
        customer_id = st.number_input("Customer ID", min_value=1, step=1)
        name = st.text_input("New Name")
        balance = st.number_input("New Balance", min_value=0.0, format="%.2f")
        if st.button("Update"):
            update_customer(customer_id, name, balance)
            st.success(f"Customer {customer_id} updated")

    elif choice == "Delete Customer":
        st.subheader("Delete Customer")
        customer_id = st.number_input("Customer ID", min_value=1, step=1)
        if st.button("Delete"):
            delete_customer(customer_id)
            st.success(f"Customer {customer_id} deleted")

    elif choice == "Credit Balance":
        st.subheader("Credit Balance")
        customer_id = st.number_input("Customer ID", min_value=1, step=1)
        amount = st.number_input("Amount to Credit", min_value=0.0, format="%.2f")
        if st.button("Credit"):
            credit_balance(customer_id, amount)
            st.success(f"Credited {amount} to customer {customer_id}")

    elif choice == "Debit Balance":
        st.subheader("Debit Balance")
        customer_id = st.number_input("Customer ID", min_value=1, step=1)
        amount = st.number_input("Amount to Debit", min_value=0.0, format="%.2f")
        if st.button("Debit"):
            debit_balance(customer_id, amount)
            st.success(f"Debited {amount} from customer {customer_id}")

    elif choice == "Bank Statement":
        st.subheader("Bank Statement")
        customers = view_customers()
        df = pd.DataFrame(customers, columns=["ID", "Name", "Balance"])
        st.dataframe(df.style.set_properties(**{'background-color': 'lightgreen', 'color': 'black'}))

if __name__ == "__main__":
    main()