

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
       background-color: Violet;
       }
        </style>
       """
st.markdown(page_bg, unsafe_allow_html=True)
#---------------------------------------------
#Metric Cards Customization-->
# CSS for colorful metric cards
st.markdown("""
<style>

/* Metric card styling */
div[data-testid="stMetric"] {
    background-color: lightyellow;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #FFB6C1;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
    text-align: center;
}

/* Metric label */
div[data-testid="stMetricLabel"] {
    color: #6A1B4D;
    font-size: 25px;
    font-weight: bold;
}

/* Metric value */
div[data-testid="stMetricValue"] {
    color: #C2185B;
    font-size: 32px;
    font-weight: bold;
}

/* Delta styling */
div[data-testid="stMetricDelta"] {
    font-size: 18px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)
#----------------------------------------------



