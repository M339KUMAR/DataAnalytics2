  

import streamlit as st
import pandas as pd 
import numpy as np 

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

#------------------------

#-----------------------------------------------
from Auth import check_login
check_login()
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Gender Risk Analysis",
    page_icon="🏢",
    layout="wide"
)

page_bg = """
       <style>
       [data-testid="stAppViewContainer"] {
       background-color: lightgrey;
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
#filtered_df= df
#----------------------Attrition Flag------------
df["Attrition_Flag"] = (
    df["Attrition"]
    .astype(int)
) 
#------------------------------------------
#          ENCODE VARIABLES
#------------------------------------------
categorical_cols = df.select_dtypes(
    include="object"
).columns.tolist()

if "Attrition" in categorical_cols:
    categorical_cols.remove("Attrition")

encoder = LabelEncoder()

for col in categorical_cols:
    df[col] = encoder.fit_transform(
        df[col].astype(str)
    ) 
# -----------------------------------------------------
# MODEL
# -----------------------------------------------------
X = df.drop(
    columns=[
        "Attrition",
        "Attrition_Flag"
    ],
    errors="ignore"
)

y = df["Attrition_Flag"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
#--------------
st.write(
    X.select_dtypes(
        include="object"
    ).columns.tolist()
)
#---------------
model.fit(X, y)
#st.write(model.classes_)

# -----------------------------------------------------
# RISK SCORE
# -----------------------------------------------------
risk_prob = model.predict_proba(X)[:, 1]
df["Risk_Probability"] == risk_prob
# -----------------------------------------------------
# RISK CATEGORY
# -----------------------------------------------------
conditions = [
    risk_prob < 0.30,
    (risk_prob >= 0.30)
    & (risk_prob <= 0.60),
    risk_prob > 0.60
]

choices = [
    "Low",
    "Medium",
    "High"
]

df["Risk_Category"] = np.select(
    conditions,
    choices
)
#-----------------------------------------------
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
        "Palo Alto Networks Employee Dataset"
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
with tab2:

    st.subheader(
        "Gender Risk Analysis"
    )

    gender_summary = (
        filtered_df.groupby("Gender").agg(
            Avg_Risk=(
                "Risk_Probability",
                "mean"
            ),

            Attrition_Rate=(
                "Attrition_Flag",
                "mean"
            ),

            Employee_Count=(
                "Gender",
                "count"
            )
        )
        .reset_index()
    )

    st.dataframe(
        gender_summary,
        use_container_width=True
    )


#Gender Detail Statistics 
with st.expander(
    "Detailed Gender Statistics"
):

    st.write(
        gender_summary.describe()
    )


#Department Wise Gender Analysis
with st.expander(
    "Department Wise Gender Analysis"
):

    dept_gender = (
        filtered_df.groupby(
            [
                "Department",
                "Gender"
            ]
        )
        .size()
        .reset_index(
            name="Employees"
        )
    )

    st.dataframe(
        dept_gender,
        use_container_width=True
    )














