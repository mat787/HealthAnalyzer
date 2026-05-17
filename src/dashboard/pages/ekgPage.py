import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

from src.utils.ekg import *
st.set_page_config(layout="wide")

st.title("EKG Analyzer")
st.header("Wstaw swój plik EKG poniżej")

plik = st.file_uploader("Wstaw plik ","csv",False)
if plik is not None:
    raw,signals,info,plt = load_ecg(plik)
    st.pyplot(plt)
    show_ecg(raw, signals['ECG_Clean'], info['ECG_R_Peaks'],512)
