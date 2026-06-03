 
import streamlit as st
import pandas as pd 
import openpyxl
import os
from PIL import Image
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components
#from streamlit_ydata_profiling import st_profile_report

#--------------------------------------------------
#---------------------------------------------------
#---------------------------------------------------
#                  LOGIN UID-PSWD
#----------------------------------------------------
import streamlit as st
# -----------------------------
# LOGIN CREDENTIALS
# -----------------------------

USER_CREDENTIALS = {
    "admin": "admin123",
    "hrmanager": "hr2026"
}

# -----------------------------
# SESSION STATE
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -----------------------------
# LOGIN SCREEN
# -----------------------------

if not st.session_state.logged_in:

    st.title("🔐 HR Analytics Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if (
            username in USER_CREDENTIALS
            and
            USER_CREDENTIALS[username] == password
        ):

            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid Username or Password")

    st.stop()
# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* Move page navigation downward */
[data-testid="stSidebarNav"] {
    padding-top: 110px;
}

/* Add icon + text together at top */
[data-testid="stSidebarNav"]::before {
    content: "HR Analytics";
    white-space: pre-line;
    display: block;
    text-align: center;
    font-size: 24px;
    font-weight: 900 !important;
    padding-top: 120px;
    margin-bottom: 0px;

    background-image: url("https://cdn-icons-png.flaticon.com/512/3135/3135715.png");
    background-repeat: no-repeat;
    background-position: top center;
    background-size: 125px;
}

</style>
""", unsafe_allow_html=True)

#--------------------------------------
#Image Icons Display-->
image_path1 = "HR_Dept_1.jpeg"
image_path2 = "graph_bar-chart.jpeg"

if os.path.exists(image_path1) & os.path.exists(image_path2):
    img1 = Image.open(image_path1)
    img1 = img1.resize((300, 150))
    img2 = Image.open(image_path2)
    img2 = img2.resize((300,150)) 
 
    # st.image([img1,img2] use_column_width=False)
    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        st.image(img1, use_column_width=True)
    with col2:
        st.image(img2, use_column_width=True)
    with col3:
        st.write("HR Data Analysis \n Helps Manager of HR Dept to \n Predict The Risk of Employees leaving the Company & Accordingly Plan Ahead To take necessary steps of Advt-Recruit-Train-Payroll and so on")
else:
    st.error(f"Image not found: {image_path}")
#--------------------------------------
# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
#--------------------------------------
#Metric Cards Customization-->
# CSS for colorful metric cards
st.markdown("""
<style>

/* Metric card styling */
div[data-testid="stMetric"] {
    background-color: #FFD1DC;
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

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
#st.sidebar.image(
#    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
#    width=120
#)

#st.sidebar.title("HR Analytics")

#page = st.sidebar.radio(
#    "Navigation",
#    [
#        "Home",
#        "Executive Dashboard",
#        "Employee Risk Profile",
#        "Department Risk Analysis",
#        "Explainability",
#        "Model Performance"
#    ]
#)

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------
#if page == "Home":

page_bg = """
       <style>
       [data-testid="stAppViewContainer"] {
       background-color: lightblue;
       }
        </style>
       """
st.markdown(page_bg, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>UNIFIED MENTOR</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'> Data Analytics Intern</h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'> Project-2: HR Analytics</h2>", unsafe_allow_html=True)
    
 
st.markdown(
        '<p class="main-title">HR Analytics Dashboard</p>',
        unsafe_allow_html=True
    )

st.markdown(
        '<p class="sub-title">'
        'Predict Employee Attrition Risk using Machine Learning'
        '</p>',
        unsafe_allow_html=True
    )

st.markdown("---")

st.subheader("📌 Problem Statement")

st.write("""
    **Palo Alto Networks** faces major HR challenges such as:

    - Sudden and unanticipated resignations
    - Loss of high-performing or critical employees
    - Reactive countermeasures that come too late
    """)

st.subheader("🎯 Organizational Need")

st.write("""
    The organization requires:

    - A systematic way to predict employee attrition risk
    - Quantitative risk scores for employees
    - Visibility into key drivers influencing exit decisions
    """)

st.subheader("⚙️ Methodology")

st.markdown("""
    #### 1. Data Preprocessing
    - Encode categorical variables
    - Scale numerical columns
    - Handle class imbalance using **SMOTE**
    - Train-test split using **stratification**

    #### 2. Feature Engineering
    - Income-to-Experience Ratio
    - Promotion Delay Indicator
    - Engagement Composite Score
    - Workload Stress Flag

    #### 3. Model Development
    - Baseline Model → Logistic Regression
    - Advanced Models → Random Forest, XGBoost

    #### 4. Model Evaluation
    - Accuracy
    - Precision
    - Recall
    - F1 Score
    - ROC-AUC

    #### 5. Risk Scoring Framework
    - **Low Risk:** < 30%
    - **Medium Risk:** 30% – 60%
    - **High Risk:** > 60%
    """)

st.markdown("---")

st.subheader("📂 Dataset Information")

col1, col2, col3 = st.columns(3)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Features",
        value="31"
    )

with col2:
    st.metric(
        label="Target Variable",
        value="Attrition"
    )

with col3:
    st.metric(
        label="Company",
        value="Palo Alto"
    )

st.markdown("---")

df1 = pd.read_excel('Palo Alto Networks.xlsx', engine='openpyxl')
st.write("***📌Palo Alto Networks Dataset***")
st.dataframe(df1)
 
    # Convert object columns to string
    #for col in df1.select_dtypes(include="object").columns:
    #    df1[col] = df1[col].fillna("Missing")
    #    df1[col] = df1[col].astype(str)

st.write("***EXPLORATORY DATA ANALYSIS***")
if st.button("Generate EDA Report"):
    with st.spinner("Generating EDA Report... Please wait"):
        try:
             df_report = df1.copy()

             # Fix object columns
             for col in df_report.select_dtypes(include="object").columns:
                 df_report[col] = (
                                  df_report[col]
                                  .fillna("Missing")
                                  .astype(str)
                                  )

             profile = ProfileReport(
                                  df_report,
                                  explorative=True,
                                  minimal=True
                                 )

             # Save report
             profile.to_file("EDA_Report.html")

             st.success("EDA Report Generated Successfully")

             # Download button
             with open("EDA_Report.html", "rb") as file:
                  st.download_button(
                          label="Download EDA Report",
                          data=file,
                          file_name="EDA_Report.html",
                          mime="text/html"
                          )

        except Exception as e:
                 st.error(f"Error: {e}")
 
st.success(
        "Use the sidebar to navigate through the dashboard modules."
    )
# ---------------------------------------------------
# PAGE ROUTING MESSAGE
# ---------------------------------------------------
#else:
    #st.title(page)

    #st.info(
    #    f"The **{page}** page will be created in "
    #    f"`pages/{page.replace(' ', '_')}.py`"
    #)















