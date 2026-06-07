   
import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px

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
    page_title="👤Employee Gender Risk Analysis",
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
st.subheader(" 👤 Employee Risk Analysis based on Gender:")
st.divider()
#------------------Load Dataframe----------------
# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Palo Alto Networks.xlsx")
    return df
  
df = load_data()
#st.dataframe(df)
# --------------------------------------------------
# METRICS
# --------------------------------------------------

total_employees = len(df)

male_employees = (
    df["Gender"] == "Male"
).sum()

female_employees = (
    df["Gender"] == "Female"
).sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Employees",
        total_employees
    )

with col2:
    st.metric(
        "Male Employees",
        male_employees
    )

with col3:
    st.metric(
        "Female Employees",
        female_employees
    )

#-----------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "📋 Dataset Explorer",
        "👥 Gender Insights",
        "📊 Gender Visuals"
    ]
)

#-------------------Tab 1--------------------------
with tab1:

    st.subheader("Complete Employee Dataset")

    st.dataframe(
        df,
        use_container_width=True
    )

    gender_filter = st.selectbox(
        "Select Gender",
        ["Male", "Female"]
    )

    gender_df = df[
        df["Gender"] == gender_filter
    ]

    st.subheader(
        f"{gender_filter} Employees"
    )

    st.dataframe(
        gender_df,
        use_container_width=True
    )
#--------------------Tab 2 ------------------------
with tab2:

    st.subheader(
        "Gender & Department Analysis"
    )

    col1, col2 = st.columns(2)

    with col1:
        gender_choice = st.selectbox(
            "Select Gender",
            ["Male", "Female"],
            key="gender_tab2"
        )

    with col2:
        department_choice = st.selectbox(
            "Select Department",
            sorted(
                df["Department"]
                .unique()
            )
        )

    filtered_df = df[
        (df["Gender"] == gender_choice)
        &
        (df["Department"] == department_choice)
    ]

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.write(
        f"Records Found : {len(filtered_df)}"
    )

st.divider()

st.subheader(
        "Department-wise Gender Distribution"
    )
# ==================================
    # MALE EMPLOYEES BY DEPARTMENT
# ==================================
male_df = (
        df[
            df["Gender"] == "Male"
        ]
        .groupby("Department")
        .size()
        .reset_index(
            name="Employee_Count"
        )
    )

fig_male = px.bar(
        male_df,
        x="Department",
        y="Employee_Count",
        text="Employee_Count",
        color="Department",
        title="Male Employees Across Departments"
    )

fig_male.update_traces(
        textposition="outside"
    )

st.plotly_chart(
        fig_male,
        use_container_width=True
    )

# ==================================
    # FEMALE EMPLOYEES BY DEPARTMENT
# ==================================
female_df = (
        df[
            df["Gender"] == "Female"
        ]
        .groupby("Department")
        .size()
        .reset_index(
            name="Employee_Count"
        )
    )

fig_female = px.bar(
        female_df,
        x="Department",
        y="Employee_Count",
        text="Employee_Count",
        color="Department",
        title="Female Employees Across Departments"
    )

fig_female.update_traces(
        textposition="outside"
    )

st.plotly_chart(
        fig_female,
        use_container_width=True
    )
#------------------------Tab 3---------------------
df_model = df.copy()

categorical_cols = (
    df_model.select_dtypes(
        include="object"
    )
    .columns
    .tolist()
)

if "Attrition" in categorical_cols:
    categorical_cols.remove(
        "Attrition"
    )

encoder = LabelEncoder()

for col in categorical_cols:
    df_model[col] = encoder.fit_transform(
        df_model[col].astype(str)
    )

X = df_model.drop(
    columns=["Attrition"],
    errors="ignore"
)

y = df_model["Attrition"].astype(int)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

df["Risk_Probability"] = (
    model.predict_proba(X)[:, 1]
)           
#-------------------------------------------
with tab3:

    st.subheader(
        "Risk Probability Analysis"
    )

    gender_risk = (
        df.groupby("Gender")
        ["Risk_Probability"]
        .mean()
        .reset_index()
    )

    fig1 = px.bar(
        gender_risk,
        x="Gender",
        y="Risk_Probability",
        color="Gender",
        text_auto=".2%"
    )

    fig1.update_layout(
        title="Average Risk Probability by Gender"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )
#----------------------------------------------
dept_gender = (
        df.groupby(
            [
                "Department",
                "Gender"
            ]
        )
        .size()
        .reset_index(
            name="Employee_Count"
        )
    )

fig2 = px.bar(
        dept_gender,
        x="Department",
        y="Employee_Count",
        color="Gender",
        barmode="group",
        text_auto=True
    )

fig2.update_layout(
        title="Department-wise Male & Female Employee Count"
    )

st.plotly_chart(
        fig2,
        use_container_width=True
    )
#---------------------------------------------         
                











