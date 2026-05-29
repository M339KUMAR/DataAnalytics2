

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
