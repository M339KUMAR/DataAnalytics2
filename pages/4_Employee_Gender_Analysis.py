

import streamlit as st
import pandas as pd 
import numpy as np 


#-----------------------------------------------
from Auth import check_login
check_login()
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Department Risk Analysis",
    page_icon="🏢",
    layout="wide"
)

page_bg = """
       <style>
       [data-testid="stAppViewContainer"] {
       background-color: cyan;
       }
        </style>
       """
st.markdown(page_bg, unsafe_allow_html=True)
#--------------------------------------
#Metric Cards Customization-->
# CSS for colorful metric cards
st.markdown("""
<style>

/* Metric card styling */
div[data-testid="stMetric"] {
    background-color: LightPink;
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
#--------------------------------------

#------------------Load Dataframe----------------
# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Palo Alto Networks.xlsx")
    return df
  
df = load_data()
filtered_df= df
#-------------------------------------------------
#    Tab - 1
#-------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    [
        "📋 Dataset",
        "👥 Gender Insights",
        "📊 Visual Analytics"
    ]
)

with tab1:

    st.subheader(
        "Employee Dataset"
    )

    with st.expander(
        "View Dataset",
        expanded=False
    ):
        st.dataframe(
            filtered_df,
            use_container_width=True
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Employees",
            len(filtered_df)
        )

    with col2:
        st.metric(
            "Male Employees",
            (
                filtered_df["Gender"]
                == "Male"
            ).sum()
        )

    with col3:
        st.metric(
            "Female Employees",
            (
                filtered_df["Gender"]
                == "Female"
            ).sum()
        )
#-------------------------------------------------
#    Tab - 2
#-------------------------------------------------
