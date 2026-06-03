

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve
)

from imblearn.over_sampling import SMOTE

#-----------------------------------------
st.set_page_config(
    page_title="Model Performance",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Model Performance Evaluation")
#--------------------------------------------
page_bg = """
       <style>
       [data-testid="stAppViewContainer"] {
       background-color: lightgreen;
       }
        </style>
       """
st.markdown(page_bg, unsafe_allow_html=True)
#--------------------------------------------
#--------------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel(
        "Palo Alto Networks.xlsx"
    )

df = load_data()
#---------------------------------------------
#Metric Cards Customization-->
# CSS for colorful metric cards
st.markdown("""
<style>

/* Metric card styling */
div[data-testid="stMetric"] {
    background-color: pink;
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

#---------------------------------------------
df["Attrition_Flag"] = (
    df["Attrition"]
    .astype(int)
)
#--------------------------------------------
categorical_cols = (
    df.select_dtypes(
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
    df[col] = encoder.fit_transform(
        df[col].astype(str)
    )
#--------------------------------------------

st.subheader(
    "Dataset Overview"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Records",
        len(df)
    )

with col2:
    st.metric(
        "Features",
        len(df.columns)-1
    )

with col3:
    st.metric(
        "Target",
        "Attrition"
    )
#--------------------------------------------
st.subheader(
    "Class Distribution"
)

class_counts = (
    df["Attrition_Flag"]
    .value_counts()
)

fig = px.pie(
    values=class_counts.values,
    names=["Stay","Leave"],
    title="Attrition Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.write(class_counts)

#--------------------------------------------
X = df.drop(
    columns=[
        "Attrition",
        "Attrition_Flag"
    ],
    errors="ignore"
)

y = df["Attrition_Flag"]

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )
)
#--------------------------------------------

smote = SMOTE(
    random_state=42
)

X_train_smote, y_train_smote = (
    smote.fit_resample(
        X_train,
        y_train
    )
)
#---------------------------------------------
st.subheader(
    "SMOTE Balancing"
)

before = pd.DataFrame(
    y_train.value_counts()
)

after = pd.DataFrame(
    y_train_smote.value_counts()
)

col1, col2 = st.columns(2)

with col1:
    st.write(
        "Before SMOTE"
    )
    st.write(before)

with col2:
    st.write(
        "After SMOTE"
    )
    st.write(after)
#--------------------------------------------
st.subheader("Model Training")

lr_model = LogisticRegression(
    random_state=42,
    max_iter=1000
)

lr_model.fit(
    X_train_smote,
    y_train_smote
)

lr_pred = lr_model.predict(X_test)

lr_prob = lr_model.predict_proba(X_test)[:,1]
#----------------------------------------------
rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(
    X_train_smote,
    y_train_smote
)

rf_pred = rf_model.predict(X_test)

rf_prob = rf_model.predict_proba(X_test)[:,1]
#---------------------------------------------
xgb_model = XGBClassifier(
    random_state=42,
    eval_metric="logloss"
)

xgb_model.fit(
    X_train_smote,
    y_train_smote
)

xgb_pred = xgb_model.predict(X_test)

xgb_prob = xgb_model.predict_proba(X_test)[:,1]
#-----------------------------------------------
def get_metrics(
    y_true,
    y_pred,
    y_prob
):

    return {
        "Accuracy":
            accuracy_score(
                y_true,
                y_pred
            ),

        "Precision":
            precision_score(
                y_true,
                y_pred
            ),

        "Recall":
            recall_score(
                y_true,
                y_pred
            ),

        "F1 Score":
            f1_score(
                y_true,
                y_pred
            ),

        "ROC AUC":
            roc_auc_score(
                y_true,
                y_prob
            )
    }
#---------------------------------------------
lr_metrics = get_metrics(
    y_test,
    lr_pred,
    lr_prob
)

rf_metrics = get_metrics(
    y_test,
    rf_pred,
    rf_prob
)

xgb_metrics = get_metrics(
    y_test,
    xgb_pred,
    xgb_prob
)
#------------------------------------------------
comparison_df = pd.DataFrame(
    [
        lr_metrics,
        rf_metrics,
        xgb_metrics
    ],
    index=[
        "Logistic Regression",
        "Random Forest",
        "XGBoost"
    ]
)

st.subheader(
    "Model Comparison"
)

st.dataframe(
    comparison_df.style.format(
        "{:.3f}"
    )
)
st.write("* Definetly from above table XGBOOST model has better performing Metrics But as a standard i have selected Random Forest Metrics for Display")
#-------------------------------------------------------------------------------------------------------------------------------------------------
st.subheader(
    "Random Forest Metrics"
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Accuracy",
        f"{rf_metrics['Accuracy']:.3f}"
    )

with col2:
    st.metric(
        "Precision",
        f"{rf_metrics['Precision']:.3f}"
    )

with col3:
    st.metric(
        "Recall",
        f"{rf_metrics['Recall']:.3f}"
    )

with col4:
    st.metric(
        "F1 Score",
        f"{rf_metrics['F1 Score']:.3f}"
    )

with col5:
    st.metric(
        "ROC AUC",
        f"{rf_metrics['ROC AUC']:.3f}"
    )
#--------------------------------------------

st.subheader(
    "Confusion Matrix"
)

cm = confusion_matrix(
    y_test,
    rf_pred
)

fig_cm = ff.create_annotated_heatmap(
    z=cm,
    x=[
        "Predicted Stay",
        "Predicted Leave"
    ],
    y=[
        "Actual Stay",
        "Actual Leave"
    ],
    showscale=True
)

st.plotly_chart(
    fig_cm,
    use_container_width=True
)
#-------------------------------------------

st.subheader(
    "ROC Curve"
)

fpr, tpr, _ = roc_curve(
    y_test,
    rf_prob
)

roc_df = pd.DataFrame({
    "False Positive Rate": fpr,
    "True Positive Rate": tpr
})

fig_roc = px.line(
    roc_df,
    x="False Positive Rate",
    y="True Positive Rate",
    title=f"ROC Curve (AUC = {rf_metrics['ROC AUC']:.3f})"
)

fig_roc.add_shape(
    type="line",
    x0=0,
    y0=0,
    x1=1,
    y1=1,
    line=dict(
        dash="dash"
    )
)

st.plotly_chart(
    fig_roc,
    use_container_width=True
)
#---------------------------------------------

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

#st.sidebar.success(
#    f"Welcome, {username}"
#)
if "username" in st.session_state:
    st.sidebar.success(
        f"Welcome, {st.session_state.username}"
    )












