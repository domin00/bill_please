import streamlit as st


def upload_bill():
    bill = st.file_uploader("Upload Bill")

    if bill:
        st.image(bill)