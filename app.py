# app.py
import streamlit as st
from modules.participants import name_input_component


def main():
    st.title('''"Bill, Please!"''')

    # Module 1: Participant Management
    name_input_component()

    # # Module 2: Image Upload and Content Extraction
    # upload_bill()

    # # Module 3: Mathematical Computations for Bill Splitting
    # split_bill(participants, bill_positions)  # You need to define bill_positions

if __name__ == "__main__":
    main()
