

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="Employee Risk Profile",
    page_icon="👤",
    layout="wide"
)

st.title("👤 Employee Risk Profile")
st.markdown(
    "Analyze employee attrition risk profile."
)

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------
@st.cache_data
def load_data():
     df = pd.read_excel("Palo Alto Networks.xlsx")
    return df

df = load_data()

# -----------------------------------------------------
# VISUAL COPY
# -----------------------------------------------------
df_visual = df.copy()

# -----------------------------------------------------
# CLEAN TARGET
# -----------------------------------------------------
df["Attrition"] = (
    df["Attrition"]
    .astype(str)
    .str.strip()
    .str.lower()
)

df["Attrition_Flag"] = (
    (df["Attrition"] == "yes")
    .astype(int)
)

# -----------------------------------------------------
# ENCODE CATEGORICALS
# -----------------------------------------------------
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

model.fit(X, y)

# -----------------------------------------------------
# RISK SCORE
# -----------------------------------------------------
risk_prob = model.predict_proba(X)[:, 1]

df["Risk_Probability"] = (
    risk_prob * 100
)

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

# -----------------------------------------------------
# COPY TO VISUAL DF
# -----------------------------------------------------
df_visual["Risk_Probability"] = (
    df["Risk_Probability"]
)

df_visual["Risk_Category"] = (
    df["Risk_Category"]
)

# -----------------------------------------------------
# EMPLOYEE SELECTOR
# -----------------------------------------------------
employee_index = st.selectbox(
    "Select Employee",
    options=df_visual.index
)

employee = df_visual.loc[
    employee_index
]

# -----------------------------------------------------
# KPI METRICS
# -----------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Risk Probability",
        f"{employee['Risk_Probability']:.2f}%"
    )

with col2:
    st.metric(
        "Risk Category",
        employee["Risk_Category"]
    )

with col3:
    st.metric(
        "Monthly Income",
        f"${employee['MonthlyIncome']:,.0f}"
    )

st.divider()

# -----------------------------------------------------
# EMPLOYEE DETAILS
# -----------------------------------------------------
st.subheader(
    "Employee Details"
)

employee_details = pd.DataFrame({
    "Feature": employee.index,
    "Value": employee.values
})

st.dataframe(
    employee_details,
    use_container_width=True
)

# -----------------------------------------------------
# FEATURE IMPORTANCE
# -----------------------------------------------------
st.subheader(
    "Top Risk Drivers"
)

importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance":
    model.feature_importances_
})

importance_df = (
    importance_df
    .sort_values(
        by="Importance",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    importance_df,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Top 10 Risk Drivers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------------------------
# RISK PROGRESS BAR
# -----------------------------------------------------
st.subheader(
    "Employee Risk Score"
)

st.progress(
    float(
        employee["Risk_Probability"]
    ) / 100
)

st.write(
    f"Risk Probability: "
    f"{employee['Risk_Probability']:.2f}%"
)
