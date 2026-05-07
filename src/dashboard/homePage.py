import streamlit as st
import time
from src.utils.parser import *
from src.database.setup_db import short_names

st.title("Apple Health Analyzer")
st.header("Wstaw swój plik Apple Health poniżej")


plik = st.file_uploader("wstaw plik","xml",False)
if plik is not None:

    load_all_health_data(plik,short_names)
    bar = st.progress(0,"analizujemy twoje dane")

    for percent_complete in range(50):
        time.sleep(0.05)
        bar.progress(percent_complete + 1)
        percent_complete = percent_complete + 1
    time.sleep(1)

    for percent_complete in range(50,100):

        time.sleep(0.05)
        bar.progress(percent_complete + 1)
        percent_complete = percent_complete + 1
    time.sleep(1)

    bar.progress(100)
    bar.empty()

    st.switch_page("pages/goalPage.py")


