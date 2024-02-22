import streamlit as st


def upload_bill():
    picture = st.camera_input("Take a picture")

    if picture:
        st.image(picture)