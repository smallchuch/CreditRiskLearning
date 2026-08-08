import streamlit as st
import plotly.express as px
import pandas as pd
import os
import sys

def find_repo_root(start, repo_name='CreditRiskLearning'):
    path = os.path.abspath(start)
    while True:
        if os.path.basename(path) == repo_name:
            return path
        parent = os.path.dirname(path)
        if parent == path:
            raise FileNotFoundError(f"Could not find repo root: {repo_name}")
        path = parent


repo_root = find_repo_root(os.getcwd())
sys.path.append(os.path.join(repo_root, 'Core Resources'))
sys.path.append(os.path.join(repo_root, 'Core Resources', 'Scripts'))

DATA_PATH = os.path.join(repo_root, 'Datasets', 'Home Credit Default Risk', 'application_train.csv')

df = pd.read_csv(DATA_PATH)
print(f"Loaded {df.shape[0]:,} rows × {df.shape[1]} columns from {DATA_PATH}")

desc = pd.read_csv('../../../Datasets/Home Credit Default Risk/HomeCredit_columns_description.csv', sep=',', encoding='cp1252')    

import streamlit as st

st.title("My Dashboard")                    # text

st.title("Portfolio Analysis")

tab_demo, tab_default, tab_credit = st.tabs(["Demographics", "Default", "Credit"])

with tab_demo:
    st.header("Demographics")
    st.write("Age, income, region breakdowns go here")

with tab_default:
    st.header("Default")
    c1, c2, c3 = st.columns(3)
    c1.metric("Default rate", "4.2%")
    c2.metric("Total defaults", "1,284")
    c3.metric("Avg PD", "3.8%")

with tab_credit:
    st.header("Credit")
    st.write("Scores, limits, utilisation go here")