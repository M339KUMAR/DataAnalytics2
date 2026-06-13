

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
       background-color: Violet
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

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel(
        "Palo Alto Networks.xlsx"
    )

df = load_data()
#---------------------------------------------------
st.markdown("---")
#-----------------------------------------------

# --------------------------------------------------
# SATISFACTION METRICS
# --------------------------------------------------

avg_job_sat = round(
    df["JobSatisfaction"].mean(),
    2
)

avg_env_sat = round(
    df["EnvironmentSatisfaction"].mean(),
    2
)

avg_rel_sat = round(
    df["RelationshipSatisfaction"].mean(),
    2
)

avg_wlb = round(
    df["WorkLifeBalance"].mean(),
    2
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Job Satisfaction",
        avg_job_sat
    )

with col2:
    st.metric(
        "Environment Satisfaction",
        avg_env_sat
    )

with col3:
    st.metric(
        "Relationship Satisfaction",
        avg_rel_sat
    )

with col4:
    st.metric(
        "Work-Life Balance",
        avg_wlb
    )
#---------------------------------------------------
#------------------TABS------------------------------
st.markdown("---")

tab1, tab2, tab3 = st.tabs(
    [
        "📋 Satisfaction Overview",
        "🏢 Department Analysis",
        "📊 Satisfaction Visuals"
    ]
)
#-----------------------------------------------
#---------------------- ( TAB-1 ) --------------
with tab1:

    st.subheader(
        "Employee Satisfaction Dataset"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.markdown("---")

    satisfaction_level = st.selectbox(
        "Select Job Satisfaction Level",
        sorted(
            df["JobSatisfaction"].unique()
        )
    )

    filtered_df = df[
        df["JobSatisfaction"]
        == satisfaction_level
    ]

    st.write(
        f"Employees with Job Satisfaction = {satisfaction_level}"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader(
        "Summary Statistics"
    )

    st.dataframe(
        df[
            [
                "JobSatisfaction",
                "EnvironmentSatisfaction",
                "RelationshipSatisfaction",
                "WorkLifeBalance"
            ]
        ].describe(),
        use_container_width=True
    )
#--------------------------------------------------
#---------------------- ( TAB-2 ) ------------------

with tab2:

    st.subheader(
        "Department-wise Satisfaction Analysis"
    )

    dept_job = (
        df.groupby("Department")
        ["JobSatisfaction"]
        .mean()
        .reset_index()
    )

    fig1 = px.bar(
        dept_job,
        x="Department",
        y="JobSatisfaction",
        color="Department",
        text_auto=".2f",
        title="Average Job Satisfaction by Department"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    dept_env = (
        df.groupby("Department")
        ["EnvironmentSatisfaction"]
        .mean()
        .reset_index()
    )

    fig2 = px.bar(
        dept_env,
        x="Department",
        y="EnvironmentSatisfaction",
        color="Department",
        text_auto=".2f",
        title="Average Environment Satisfaction by Department"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    dept_wlb = (
        df.groupby("Department")
        ["WorkLifeBalance"]
        .mean()
        .reset_index()
    )

    fig3 = px.bar(
        dept_wlb,
        x="Department",
        y="WorkLifeBalance",
        color="Department",
        text_auto=".2f",
        title="Average Work-Life Balance by Department"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

#--------------------------------------------------
#---------------------- ( TAB-3 ) ------------------
with tab3:

    st.subheader(
        "Satisfaction Visual Analytics"
    )

    fig4 = px.histogram(
        df,
        x="JobSatisfaction",
        nbins=4,
        title="Job Satisfaction Distribution"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    fig5 = px.histogram(
        df,
        x="EnvironmentSatisfaction",
        nbins=4,
        title="Environment Satisfaction Distribution"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    fig6 = px.box(
        df,
        x="Department",
        y="JobSatisfaction",
        color="Department",
        title="Department vs Job Satisfaction"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

    fig7 = px.box(
        df,
        x="Gender",
        y="JobSatisfaction",
        color="Gender",
        title="Gender vs Job Satisfaction"
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )
#--------------------------------------------------
#--------------------------------------------------

df["Satisfaction_Score"] = (
    df["JobSatisfaction"]
    + df["EnvironmentSatisfaction"]
    + df["RelationshipSatisfaction"]
    + df["WorkLifeBalance"]
) / 4
#--------------------------------------------------

top_10 = (
    df.sort_values(
        "Satisfaction_Score",
        ascending=False
    )
    .head(10)
)

bottom_10 = (
    df.sort_values(
        "Satisfaction_Score"
    )
    .head(10)
)
#---------------------------------------------------

with st.expander(
    "🏆 Top 10 Most Satisfied Employees"
):
    st.dataframe(top_10)

with st.expander(
    "⚠️ Bottom 10 Least Satisfied Employees"
):
    st.dataframe(bottom_10)
#---------------------------------------------------








