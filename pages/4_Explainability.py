

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Explainability",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Employee Attrition Explainability")
#----------------------------------------------------
page_bg = """
       <style>
       [data-testid="stAppViewContainer"] {
       background-color: lightyellow;
       }
        </style>
       """
st.markdown(page_bg, unsafe_allow_html=True)
#--------------------------------------------------------------
#--------------------------------------
#Metric Cards Customization-->
# CSS for colorful metric cards
st.markdown("""
<style>

/* Metric card styling */
div[data-testid="stMetric"] {
    background-color: lightgreen;
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

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_excel(
        "Palo Alto Networks.xlsx"
    )

df = load_data()

# --------------------------------------------------
# VISUAL COPY
# --------------------------------------------------

df2 = df.copy()

# --------------------------------------------------
# TARGET
# --------------------------------------------------

df["Attrition_Flag"] = (
    df["Attrition"]
    .astype(int)
)

# --------------------------------------------------
# ENCODE CATEGORICALS
# --------------------------------------------------

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

# --------------------------------------------------
# MODEL
# --------------------------------------------------

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

model.fit(X, y)

# --------------------------------------------------
# RISK SCORE
# --------------------------------------------------

risk_prob = model.predict_proba(X)[:,1]

df["Risk_Probability"] = risk_prob

conditions = [
    risk_prob < 0.30,
    (risk_prob >= 0.30) &
    (risk_prob <= 0.60),
    risk_prob > 0.60
]

choices = [
    "Low",
    "Medium",
    "High"
]

df["Risk_Category"] = np.select(
    conditions,
    choices,
    default="Low"
)

# --------------------------------------------------
# COPY TO VISUAL DF
# --------------------------------------------------

df2["Risk_Probability"] = (
    df["Risk_Probability"]
)

df2["Risk_Category"] = (
    df["Risk_Category"]
)

# --------------------------------------------------
# EMPLOYEE SELECTION
# --------------------------------------------------

st.sidebar.header("Employee Selection")

employee_id = st.sidebar.selectbox(
    "Select Employee",
    df2.index
)

employee = df2.loc[employee_id]

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Risk Score",
        f"{employee['Risk_Probability']:.2%}"
    )

with col2:
    st.metric(
        "Risk Category",
        employee["Risk_Category"]
    )

with col3:
    st.metric(
        "Department",
        employee["Department"]
    )

with col4:
    st.metric(
        "Job Role",
        employee["JobRole"]
    )

st.divider()

# --------------------------------------------------
# EMPLOYEE DETAILS
# --------------------------------------------------
st.subheader("Employee Details")

st.dataframe(
    employee.to_frame()
)

# --------------------------------------------------
# FEATURE IMPORTANCES
# --------------------------------------------------
st.subheader(
    "Top Factors Driving Attrition"
)

importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance_df = (
    importance_df
    .sort_values(
        by="Importance",
        ascending=False
    )
)

fig = px.bar(
    importance_df.head(10),
    x="Importance",
    y="Feature",
    orientation="h",
    title="Feature Importance"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# RISK DRIVERS
# --------------------------------------------------

st.subheader(
    "Employee Risk Drivers"
)

if employee["MonthlyIncome"] < 5000:
    st.warning(
        "Low Monthly Income may contribute to attrition."
    )

if employee["YearsSinceLastPromotion"] > 5:
    st.warning(
        "Long gap since last promotion."
    )

if employee["YearsAtCompany"] > 10:
    st.info(
        "Long tenure employee."
    )

# --------------------------------------------------
# RISK DRIVERS
# --------------------------------------------------

st.subheader(
    "HR Recommendation"
)

risk_score = employee["Risk_Probability"]

if risk_score > 0.70:
    st.error(
        "High retention risk. Immediate intervention recommended."
    )

elif risk_score > 0.40:
    st.warning(
        "Moderate retention risk. Monitor closely."
    )

else:
    st.success(
        "Low attrition risk."
    )














