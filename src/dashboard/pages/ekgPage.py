import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import sys
from pathlib import Path
from src.utils.ekg import *

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


st.set_page_config(layout="wide")

st.title("EKG Analyzer")
st.header("Wstaw swój plik EKG poniżej")

plik = st.file_uploader("Wstaw plik ","csv",False)
if plik is not None:
    raw,signals,info,plt = load_ecg(plik)
    st.pyplot(plt)
    show_ecg(raw, signals['ECG_Clean'], info['ECG_R_Peaks'],512)
