
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
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Executive HR Dashboard")
st.markdown("Monitor employee attrition risk and workforce insights")

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------
@st.cache_data
def load_data():

    df = pd.read_excel("Palo Alto Networks.xlsx")

    return df


df = load_data()

# -----------------------------------------------------
# FEATURE ENGINEERING
# -----------------------------------------------------
df["Income_Experience_Ratio"] = (
    df["MonthlyIncome"] /
    (df["TotalWorkingYears"] + 1)
)

df["Promotion_Delay"] = (
    df["YearsSinceLastPromotion"]
)

df["Engagement_Score"] = (
    df["JobSatisfaction"] +
    df["EnvironmentSatisfaction"] +
    df["RelationshipSatisfaction"]
) / 3

df["Workload_Stress_Flag"] = np.where(
    (df["OverTime"] == "Yes") &
    (df["WorkLifeBalance"] <= 2),
    1,
    0
)
st.write(df["Attrition"].head(20))
st.write(df["Attrition"].dtype)
st.write(df["Attrition"].unique())
"""
# -----------------------------------------------------
# CLEAN ATTRITION COLUMN
# -----------------------------------------------------
df["Attrition"] = (
    df["Attrition"]
    .astype(str)
    .str.strip()
    .str.lower()
)

# -----------------------------------------------------
# ENCODE TARGET
# -----------------------------------------------------
#df["Attrition_Flag"] = np.where(
#    df["Attrition"] == "Yes",
#    1,
#    0
#)
df["Attrition_Flag"] = ((df["Attrition"] == "yes").astype(int))

#categorical_cols = df.select_dtypes(
#    include="object"
#).columns.tolist()"""
# -----------------------------------------------------
# TARGET VARIABLE
# -----------------------------------------------------
if df["Attrition"].dtype == "object":

    df["Attrition"] = (
        df["Attrition"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df["Attrition_Flag"] = (
        df["Attrition"] == "yes"
    ).astype(int)

else:
    # already numeric
    df["Attrition_Flag"] = (
        df["Attrition"]
    ).astype(int)

# DEBUG
st.write(df["Attrition"].unique())
st.write(df["Attrition_Flag"].value_counts())
# -----------------------------------------------------
# DEBUG CHECK
# -----------------------------------------------------
st.write("Attrition Counts")
st.write(df["Attrition"].value_counts())

st.write("Attrition Flag Counts")
st.write(df["Attrition_Flag"].value_counts())

#categorical_cols.remove("Attrition")
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
# MODEL TRAINING FOR RISK SCORE
# -----------------------------------------------------

#-----------------------------------------------------

X = df.drop(
    columns=["Attrition", "Attrition_Flag"]
)

y = df["Attrition_Flag"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

#risk_prob = model.predict_proba(X)[:, 1]
probabilities = model.predict_proba(X)

if probabilities.shape[1] > 1:
    risk_prob = probabilities[:, 1]
else:
    risk_prob = probabilities[:, 0]

df["Risk_Score"] = risk_prob * 100

# -----------------------------------------------------
# RISK CATEGORY
# -----------------------------------------------------
def risk_category(score):

    if score < 30:
        return "Low"

    elif score <= 60:
        return "Medium"

    else:
        return "High"


df["Risk_Category"] = df[
    "Risk_Score"
].apply(risk_category)

# -----------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------
st.sidebar.header("Filters")

department = st.sidebar.multiselect(
    "Department",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)

job_role = st.sidebar.multiselect(
    "Job Role",
    options=df["JobRole"].unique(),
    default=df["JobRole"].unique()
)

risk_filter = st.sidebar.multiselect(
    "Risk Category",
    options=df["Risk_Category"].unique(),
    default=df["Risk_Category"].unique()
)

filtered_df = df[
    (df["Department"].isin(department)) &
    (df["JobRole"].isin(job_role)) &
    (df["Risk_Category"].isin(risk_filter))
]

# -----------------------------------------------------
# KPI METRICS
# -----------------------------------------------------
total_emp = len(filtered_df)

attrition_count = filtered_df[
    filtered_df["Attrition"] == "yes"
].shape[0]

attrition_rate = (
    attrition_count / total_emp
) * 100

high_risk_count = filtered_df[
    filtered_df["Risk_Category"] == "High"
].shape[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Employees",
        total_emp
    )

with col2:
    st.metric(
        "Attrition Count",
        attrition_count
    )

with col3:
    st.metric(
        "Attrition Rate %",
        f"{attrition_rate:.2f}%"
    )

with col4:
    st.metric(
        "High Risk Employees",
        high_risk_count
    )

st.markdown("---")

# -----------------------------------------------------
# CHARTS ROW 1
# -----------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    risk_chart = px.pie(
        filtered_df,
        names="Risk_Category",
        title="Employee Risk Distribution"
    )

    st.plotly_chart(
        risk_chart,
        use_container_width=True
    )

with col2:

    dept_attrition = (
        filtered_df.groupby("Department")
        ["Attrition_Flag"]
        .mean()
        .reset_index()
    )

    dept_chart = px.bar(
        dept_attrition,
        x="Department",
        y="Attrition_Flag",
        title="Department Wise Attrition Rate"
    )

    st.plotly_chart(
        dept_chart,
        use_container_width=True
    )

# -----------------------------------------------------
# CHARTS ROW 2
# -----------------------------------------------------
col3, col4 = st.columns(2)

with col3:

    role_chart = px.histogram(
        filtered_df,
        x="JobRole",
        color="Risk_Category",
        title="Risk by Job Role"
    )

    st.plotly_chart(
        role_chart,
        use_container_width=True
    )

with col4:

    overtime_chart = px.box(
        filtered_df,
        x="OverTime",
        y="MonthlyIncome",
        color="Attrition",
        title="Income vs Overtime"
    )

    st.plotly_chart(
        overtime_chart,
        use_container_width=True
    )

st.markdown("---")

# -----------------------------------------------------
# HIGH RISK EMPLOYEES
# -----------------------------------------------------
st.subheader("🚨 High Risk Employees")

high_risk_df = filtered_df[
    filtered_df["Risk_Category"] == "High"
]

display_cols = [
    "Age",
    "Department",
    "JobRole",
    "MonthlyIncome",
    "YearsAtCompany",
    "OverTime",
    "Risk_Score"
]

st.dataframe(
    high_risk_df[
        display_cols
    ].sort_values(
        by="Risk_Score",
        ascending=False
    ),
    use_container_width=True
)

# -----------------------------------------------------
# DOWNLOAD BUTTON
# -----------------------------------------------------
csv = filtered_df.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download Dashboard Data",
    data=csv,
    file_name="executive_dashboard.csv",
    mime="text/csv"
)
