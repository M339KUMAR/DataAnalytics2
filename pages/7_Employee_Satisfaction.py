

import streamlit as st



from Auth import check_login
check_login()
#-----------------------------------------
st.set_page_config(
    page_title="Employee Satisfaction",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Employee Satisfaction Statistics:")
#--------------------------------------------
page_bg = """
       <style>
       [data-testid="stAppViewContainer"] {
       background-color: lightgold;
       }
        </style>
       """
st.markdown(page_bg, unsafe_allow_html=True)
#----------------------------------------------



