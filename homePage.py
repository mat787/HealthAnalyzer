import os

import streamlit as st
import time
from parser import *


st.title("HealthAnalyzer")
st.header("Wstaw swój plik Apple Health poniżej")


plik = st.file_uploader("wstaw plik","xml",False)
if plik is not None:

    parseSleep(plik)
    bar = st.progress(0,"analizujemy twoje dane")
    percent_complete = 0
    for percent_complete in range(50):
        time.sleep(0.05)
        bar.progress(percent_complete + 1)
    time.sleep(1)
    parseHeartRate(plik)
    for percent_complete in range(50):
        time.sleep(0.05)
        bar.progress(percent_complete + 1)
    time.sleep(1)
    if os.path.getsize("sleep.csv") > 2:
        df_heart = pd.read_csv("heart_rate.csv")
        df_sleep = pd.read_csv("sleep.csv")

        st.session_state['heart_data'] = df_heart
        st.session_state['sleep_data'] = df_sleep
    else:
        df_heart = pd.read_csv("heart_rate.csv")
        st.session_state['heart_data'] = df_heart

    bar.progress(100)
    bar.empty()

    st.switch_page("pages/goalPage.py")


