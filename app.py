import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from database import *

st.set_page_config("Payment System", "💰")
create_tables()

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_admin(username, password):
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid Credentials ❌")
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("Menu")
choice = st.sidebar.radio(
    "",
    ["Add Member", "View Members", "Logout"]
)

# ---------------- ADD MEMBER ----------------
if choice == "Add Member":
    st.subheader("➕ Add Member")

    name = st.text_input("Name")
    contact = st.text_input("Contact")
    amount = st.number_input("Amount", min_value=0.0)
    paid = st.selectbox("Paid", ["No", "Yes"])
    payment_date = st.date_input("Payment Date", date.today())

    if st.button("Save"):
        if name and contact:
            add_member(name, contact, amount, paid, str(payment_date))
            st.success("Member Added 🎉")
        else:
            st.warning("Fill all fields")

# ---------------- VIEW MEMBERS ----------------
elif choice == "View Members":
    st.subheader("📋 Members List")

    data = get_members()
    df = pd.DataFrame(
        data,
        columns=["ID", "Name", "Contact", "Amount", "Paid", "Date"]
    )

    if df.empty:
        st.info("No members found")
    else:
        st.dataframe(df)

        member_id = st.selectbox(
            "Select Member ID",
            df["ID"].tolist()
        )

        selected = df[df["ID"] == member_id].iloc[0]

        st.markdown("### ✏ Edit Member Details")
        new_name = st.text_input("Name", selected["Name"])
        new_contact = st.text_input("Contact", selected["Contact"])
        new_amount = st.number_input(
            "Amount",
            value=float(selected["Amount"]),
            min_value=0.0
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Update Details"):
                update_member(
                    member_id,
                    new_name,
                    new_contact,
                    new_amount
                )
                st.success("Member Updated ✅")
                st.rerun()

        with col2:
            if st.button("🗑 Delete Member"):
                delete_member(member_id)
                st.warning("Member Deleted ❌")
                st.rerun()

# ---------------- LOGOUT ----------------
elif choice == "Logout":
    st.session_state.logged_in = False
    st.rerun()
