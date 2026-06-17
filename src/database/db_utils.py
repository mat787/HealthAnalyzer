import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


def load_record_from_db(db_path: str, data_type: str, sourceName=None):
    conn = sqlite3.connect(db_path)
    if sourceName is None:
        df = pd.read_sql("SELECT * FROM clean_record WHERE type = ?",conn, params=[data_type])
    if sourceName is 'apple':
        df = pd.read_sql("SELECT * FROM clean_record WHERE type = ? AND sourceName LIKE ?", conn, params=[data_type, sourceName])
    else:
        return None
    conn.close()
    return df
