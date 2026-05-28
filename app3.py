 
import streamlit as st
import pandas as pd 
import openpyxl
import os
from PIL import Image
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
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
st.markdown("""
<style>

.main-title {
    font-size: 40px;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
}

.sub-title {
    font-size: 22px;
    color: #4a4a4a;
    text-align: center;
}

.metric-card {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

.sidebar .sidebar-content {
    background-color: #f5f5f5;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=120
)

st.sidebar.title("HR Analytics")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Executive Dashboard",
        "Employee Risk Profile",
        "Department Risk Analysis",
        "Explainability",
        "Model Performance"
    ]
)

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------
if page == "Home":

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
    for col in df1.select_dtypes(include="object").columns:
        df1[col] = df1[col].fillna("Missing")
        df1[col] = df1[col].astype(str)

    st.write("***EXPLORATORY DATA ANALYSIS***")
    try:
       #from ydata_profiling import ProfileReport
       report = ProfileReport(df1, explorative=True, minimal=True)
       # Save report
       #profile.to_file("report.html")
       html = report.to_html()

       # Read HTML file
       #with open("report.html", "r", encoding="utf-8") as f:
       #     html = f.read()

       # Display in Streamlit
       components.html(html, 
                       height=1000, 
                       scrolling=True)
    except Exception as e: 
       st.write(f"Issue in Report Generation: {e}")
    finally :
       st.write("Generating EDA Report..")
 
    st.success(
        "Use the sidebar to navigate through the dashboard modules."
    )
# ---------------------------------------------------
# PAGE ROUTING MESSAGE
# ---------------------------------------------------
else:
    st.title(page)

    st.info(
        f"The **{page}** page will be created in "
        f"`pages/{page.replace(' ', '_')}.py`"
    )













