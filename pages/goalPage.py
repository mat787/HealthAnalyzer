import os

import streamlit as st

st.title("HealthAnalyzer")
st.header("Twoje dane")

if 'heart_data' in st.session_state:
    df = st.session_state['heart_data']
    st.write("Dane tętna:")
    st.dataframe(df)
    #st.line_chart(df['value'])
    #st.line_chart(df)
else:
    st.error("Wgraj najpierw plik XML na stronie głównej!")

if 'sleep_data' in st.session_state:
    df = st.session_state['sleep_data']
    st.write("Dane snu:")
    st.dataframe(df)
    #st.line_chart(df)
elif os.path.getsize("sleep.csv") == 2:
    st.error("Plik nie zawiera danych")
else:
    st.error("Wgraj najpierw plik XML na stronie głównej!")



