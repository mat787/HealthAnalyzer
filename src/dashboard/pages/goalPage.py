import plotly.express as px
import streamlit as st

from src.utils.utils import load_record_from_db, load_record_from_watch

st.title("HealthAnalyzer")
st.header("Twoje dane")
df=load_record_from_db('health_data.db', 'hr')
left, middle = st.columns(2)
if left.button('Wgraj wszystkie dane tętna', width="stretch"):
    df=load_record_from_db('health_data.db', 'hr')
if middle.button('Wgraj dane z tylko z zegarka apple ', width="stretch"):
    df=load_record_from_watch('health_data.db', 'hr')


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
                         label="1h",
                         step="hour",
                         stepmode="backward"),
                    dict(count=1,
                         label="1d",
                         step='day',
                         stepmode='backward'),
                    dict(count =7,
                         label="1w",
                         step="day",
                         stepmode="backward"),
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
    st.plotly_chart(fig, use_container_width=True)
    st.download_button(
        label='Pobierz swoje dane',
        data=df.to_csv(index=False),
        file_name='health_data.csv',
        mime='text/csv'
    )
    st.write(" ")


else:
    st.error("Wgraj najpierw plik XML na stronie głównej!")
