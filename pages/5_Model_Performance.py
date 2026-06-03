

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
       background-color: lightblue;
       }
        </style>
       """
st.markdown(page_bg, unsafe_allow_html=True)
#--------------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel(
        "Palo Alto Networks.xlsx"
    )

df = load_data()
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














