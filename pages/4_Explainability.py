

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









