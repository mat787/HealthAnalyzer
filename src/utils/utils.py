import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

@st.cache_data
def load_record_from_db(db_path: str, data_type: str):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(
        "SELECT * FROM clean_record WHERE type = ?",
        conn, params=[data_type]
    )

    conn.close()
    return df

def load_record_from_watch(db_path, data_type):
    conn = sqlite3.connect(db_path)
    df= pd.read_sql(
        "SELECT * FROM clean_record WHERE type = ? AND sourceName LIKE ?",
        conn, params = [data_type, '%apple%']
    )
    conn.close()
    return df



def clean_data(df, table_name):
    """Funkcja czyszcząca pojedynczy DataFrame przed zapisem jako 'clean'."""
    # 1. Usuwamy kolumny widma (None, 'None', całkowicie puste)
    cols_to_drop = [col for col in df.columns if col is None or str(col).lower() == 'none']
    df = df.drop(columns=cols_to_drop, errors='ignore')
    df = df.dropna(axis=1, how='all')

    # 2. Naprawa typów danych
    if 'value' in df.columns:
        df['value'] = pd.to_numeric(df['value'], errors='coerce')

    date_cols = ['startDate', 'endDate', 'creationDate']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # 3. Usuwanie duplikatów (Apple Health często dubluje rekordy przy imporcie)
    df = df.drop_duplicates()

    # 4. Specyficzne filtry (np. usuwanie niemożliwego tętna)
    if 'hr' in table_name and 'value' in df.columns:
        df = df[(df['value'] > 30) & (df['value'] < 250)]

    return df