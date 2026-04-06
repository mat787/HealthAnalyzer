import os
import plotly.express as px
import streamlit as st

from utils import load_data_from_db

st.title("HealthAnalyzer")
st.header("Twoje dane")
df = load_data_from_db('Health_data.db','hr')

if df is not None:

    st.write("Dane tętna:")
    st.dataframe(df)
    fig = px.line(df, x='startDate', y='value',
                  title='Tętno uśrednione (1 min)',
                  labels={'value': 'BPM', 'startDate': 'Czas'},
                  template='plotly_dark')  # pasuje do Streamlita
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    # WYŚWIETLANIE WYKRESU
    st.plotly_chart(fig, use_container_width=True)
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



