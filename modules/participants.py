import streamlit as st
import pandas as pd

def name_submit():
    st.session_state.widget = ''


def name_input_component():
    # Initialize or get existing participant data
    if 'participants_dict' not in st.session_state:
        st.session_state.participants_dict = {}
    
    st.header("Add Participants")

    # Text input for participant name
    new_name = st.text_input("Enter Participant Name", key="new_name")

    # Add button to add the name to the participant table
    col1, col2 = st.columns([1,8])
    if col1.button("Add"):
        if new_name:
            # Add the new name to the participant dictionary
            st.session_state.participants_dict[new_name] = True
            name_submit()

    if col2.button("Remove", ):
        if new_name in st.session_state.participants_dict.keys():
            # Remove the name from the participant dictionary when the remove button is pressed
            del st.session_state.participants_dict[new_name]

    # Display the list of names
    st.subheader("Participants:")
    s = ''
    names_list = list(st.session_state.participants_dict.keys())
    
    for name in names_list:
        # Display the name and a remove button next to it
        s += "- " + name + "\n"


    if s:
        st.markdown(s)
            
