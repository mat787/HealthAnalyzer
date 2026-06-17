import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

@st.cache_data


def load_record_from_df(data_type, sourceName=None):
    final_dfs = st.session_state.get("final_dfs")
    if final_dfs is not None:
        records = final_dfs.get("Record")
    else:
        records = None

    if records is not None:
        df = records.query(f"type == '{data_type}'")
        if sourceName is not None:
            df[df["sourceName"].str.contains(sourceName, case=False, na=False)]
        return df

    return None


def clean_data(df, table_name=None):
    cols_to_drop = [col for col in df.columns if col is None or str(col).lower() == 'none']
    df = df.drop(columns=cols_to_drop, errors='ignore')
    df = df.dropna(axis=1, how='all')

    if 'value' in df.columns:
        df['value'] = pd.to_numeric(df['value'], errors='coerce')

    date_cols = ['startDate', 'endDate', 'creationDate']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    df = df.drop_duplicates()

    if table_name is not None and 'hr' in table_name and 'value' in df.columns:
        df = df[(df['value'] > 30) & (df['value'] < 250)]

    return df