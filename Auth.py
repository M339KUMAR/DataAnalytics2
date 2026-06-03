
import streamlit as st

def check_login():

    if not st.session_state.get("logged_in", False):

        st.warning("Please login first.")
        st.stop()

    st.sidebar.success(
        f"Welcome, {st.session_state.username}"
    )
