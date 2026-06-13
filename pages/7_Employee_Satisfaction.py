

import strewmlit as st



from Auth import check_login
check_login()
#-----------------------------------------
st.set_page_config(
    page_title="Model Performance",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Model Performance Evaluation")
#--------------------------------------------
page_bg = """
       <style>
       [data-testid="stAppViewContainer"] {
       background-color: lightgreen;
       }
        </style>
       """
st.markdown(page_bg, unsafe_allow_html=True)
