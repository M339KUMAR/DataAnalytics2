

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



st.title("🏢 Department Risk Analysis")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Palo Alto Networks.xlsx")
    return df
  
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
# RISK PROBABILITY
# --------------------------------------------------
risk_prob = model.predict_proba(X)[:,1]

df["Risk_Probability"] = risk_prob

# --------------------------------------------------
# RISK CATEGORY
# --------------------------------------------------
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
df2["Attrition_Flag"] = (
    df["Attrition_Flag"]
)

df2["Risk_Probability"] = (
    df["Risk_Probability"]
)

df2["Risk_Category"] = (
    df["Risk_Category"]
)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("Filters")

department = st.sidebar.multiselect(
    "Department",
    options=df2["Department"].unique(),
    default=df2["Department"].unique()
)

risk_filter = st.sidebar.multiselect(
    "Risk Category",
    options=df2["Risk_Category"].unique(),
    default=df2["Risk_Category"].unique()
)

filtered_df2 = df2[
    (df2["Department"].isin(department)) &
    (df2["Risk_Category"].isin(risk_filter))
]

#st.write(filtered_df2["Risk_Probability"].describe())
#st.write(filtered_df2["Risk_Probability"].head())
# --------------------------------------------------
# KPIs
# --------------------------------------------------
col1, col2, col3 = st.columns(3)

highest_risk_dept = (
    filtered_df2.groupby("Department")
    ["Risk_Probability"]
    .mean()
    .idxmax()
)

highest_attrition_dept = (
    filtered_df2.groupby("Department")
    ["Attrition_Flag"]
    .mean()
    .idxmax()
)

avg_risk = (
    filtered_df2["Risk_Probability"]
    .mean() * 100
)

with col1:
    st.metric(
        "Highest Risk Department",
        highest_risk_dept
    )

with col2:
    st.metric(
        "Highest Attrition Department",
        highest_attrition_dept
    )

with col3:
    st.metric(
        "Average Risk %",
        f"{avg_risk:.2f}%"
    )

st.divider()


# --------------------------------------------------
# DEPARTMENT ATTRITION RATE
# --------------------------------------------------
dept_attrition = (
    filtered_df2.groupby("Department")
    ["Attrition_Flag"]
    .mean()
    .reset_index()
)

fig1 = px.bar(
    dept_attrition,
    x="Department",
    y="Attrition_Flag",
    title="Department-wise Attrition Rate",
    text_auto=True
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# --------------------------------------------------
# DEPARTMENT RISK SCORE
# --------------------------------------------------
dept_risk = (
    filtered_df2.groupby("Department", as_index=False)
    ["Risk_Probability"]
    .mean()
    #.reset_index()
)

#st.write(dept_risk)
#st.write(dept_risk.columns)
#st.write(dept_risk["Risk_Probability"])
st.write(dept_risk)
#st.write(dept_risk.dtypes)

#fig2 = px.bar(
#    dept_risk,
#    x="Department",
#    y="Risk_Probability",
#    title="Average Risk Score by Department",
#    #text_auto=True
#    text_auto=".2f"
#)
fig2 = px.bar(
    dept_risk,
    x=dept_risk["Department"].tolist(),
    y=dept_risk["Risk_Probability"].tolist(),
    #title="Average Risk Score by Department"
)
fig2.update_yaxes(range=[0, 0.25])

#fig2.update_traces(
#    text=dept_risk["Risk_Probability"].round(3),
#    textposition="outside"
#)

st.write(fig2.layout.yaxis)
st.write(fig2.data[0].x)
st.write(fig2.data[0].y)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# --------------------------------------------------
# JOB ROLE RISK
# --------------------------------------------------
job_role_risk = (
    filtered_df2.groupby("JobRole")
    ["Risk_Probability"]
    .mean()
    .reset_index()
)

fig3 = px.bar(
    job_role_risk,
    x="JobRole",
    y="Risk_Probability",
    title="Job Role Risk Ranking"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# --------------------------------------------------
# RISK DISTRIBUTION
# --------------------------------------------------
fig4 = px.box(
    filtered_df2,
    x="Department",
    y="Risk_Probability",
    color="Department",
    title="Risk Distribution Across Departments"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)




