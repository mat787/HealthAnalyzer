import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

from src.utils.ekg import *

plik = st.file_uploader("wstaw plik","csv",False)
if plik is not None:
    raw,signals,info,plt = load_ecg(plik)
    st.pyplot(plt)
    show_ecg(raw, signals['ECG_Clean'], info['ECG_R_Peaks'],512)