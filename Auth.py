 
import streamlit as st

def check_login():

    if not st.session_state.get("logged_in", False):

        st.warning("Go To Home Page & Please login first...")
        st.stop()

    #if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:

    #st.session_state.logged_in = True
    #st.session_state.username = username

    #st.rerun()

    #st.sidebar.success(
    #    f"Welcome, {st.session_state.username}"
    #)

        username = st.session_state.get(
                        "username",
                        "User"
                   )

        st.sidebar.success(
                      f"Welcome, {username}"
        )
