import sys
import plotly.express as px
import streamlit as st
import pandas as pd
import time
from pathlib import Path
import sqlite3

from src.models.ml import prepare_multivariate, find_anomaly_multivariate
from src.utils.utils import clean_data
from src.utils.variables import DB_PATH

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


st.set_page_config(layout="wide")
st.title("HealthAnalyzer")
st.header("Analiza Danych")

@st.cache_data
def load_and_clean_data(tag_type):
    conn = sqlite3.connect(DB_PATH)
    if f"clean_{tag_type}" is not None:
        table_name = f"clean_{tag_type}"
        df=pd.read_sql(f"SELECT * FROM {table_name}", conn)
        return df
    else:
        final_dfs = st.session_state.get("final_dfs")
        if final_dfs and tag_type in final_dfs:
            return clean_data(final_dfs.get(tag_type))
    return pd.DataFrame()

all_records = load_and_clean_data("Record")

if not all_records.empty:
    all_records['startDate'] = pd.to_datetime(all_records['startDate'], utc=True).dt.tz_localize(None)

    st.subheader("Eksploracja Danych")

    source_filter = st.radio("Wybierz źródło danych:", ["Wszystkie", "Tylko Apple Watch"], horizontal=True)
    
    df_filtered_records = all_records.copy()
    if source_filter == "Tylko Apple Watch":
        df_filtered_records = df_filtered_records[df_filtered_records["sourceName"].str.contains("apple", case=False, na=False)]

    available_metrics = sorted(df_filtered_records['type'].unique())
    
    selected_metric = st.selectbox("Wybierz metrykę do wyświetlenia:", available_metrics, index=available_metrics.index('hr') if 'hr' in available_metrics else 0)
    
    df_display = df_filtered_records[df_filtered_records['type'] == selected_metric].sort_values('startDate')

    fig = px.line(df_display, x='startDate', y='value', title=f'{selected_metric} w czasie',
                  template='plotly_dark', line_shape='spline') 

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step='day', stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True), type="date"
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Wykrywanie Anomalii ")
    
    min_date = df_filtered_records['startDate'].min().date()
    max_date = df_filtered_records['startDate'].max().date()
    
    date_range = st.date_input("Wybierz zakres dat do analizy:", (max_date - pd.Timedelta(days=7), max_date), min_value=min_date, max_value=max_date, format="YYYY-MM-DD")
    metrics_for_analysis = st.multiselect("Wybierz metryki do wspólnej analizy:", options=available_metrics, default=['hr', 'step', 'dist'] if all(m in available_metrics for m in ['hr', 'step', 'dist']) else [])
    
    col1_ml, col2_ml = st.columns(2)
    with col1_ml:
        resample_interval = st.selectbox("Interwał próbkowania:", ['1min','5min', '15min', '30min', '1H'], index=1, key="resample_ml")
    with col2_ml:
        contamination_level = st.slider("Czułość wykrywania:", 0.001, 0.2, 0.05, 0.005, format="%.3f")

    if st.button("Uruchom analizę wielowymiarową"):
        if metrics_for_analysis and len(date_range) == 2:
            start_date, end_date = date_range
            mask = (df_filtered_records['startDate'].dt.date >= start_date) & (df_filtered_records['startDate'].dt.date <= end_date)
            records_for_analysis = df_filtered_records[mask]

            with st.spinner(f"Przygotowuję i analizuję dane..."):
                df_merged = prepare_multivariate(records_for_analysis, metrics_for_analysis, resample_interval)
                if not df_merged.empty:
                    df_result = find_anomaly_multivariate(df_merged, contamination=contamination_level)
                    if not df_result.empty and 'anomaly' in df_result.columns:
                        anomalies_found = df_result[df_result['anomaly'] == -1]
                        st.write(f"Wykryto {len(anomalies_found)} potencjalnych anomalii:")
                        if not anomalies_found.empty:
                            st.dataframe(anomalies_found)
                            for metric in metrics_for_analysis:
                                if metric in df_result.columns:
                                    fig_anomalies = px.line(df_result, x=df_result.index, y=metric, title=f'Wyniki Analizy dla: {metric}', template='plotly_dark', line_shape='spline')
                                    fig_anomalies.add_scatter(x=anomalies_found.index, y=anomalies_found[metric], mode='markers', marker=dict(color='red', size=8, symbol='x'), name='Anomalia')
                                    st.plotly_chart(fig_anomalies, use_container_width=True)
                        else:
                            st.success(" Nie znaleziono żadnych anomalii przy tej czułości.")
                else:
                    st.warning("Brak wystarczających danych do analizy. Spróbuj dłuższego interwału próbkowania lub szerszego zakresu dat.")
        else:
            st.error("Wybierz co najmniej jedną metrykę i poprawny zakres dat.")
else:
    st.error("Wgraj najpierw plik XML na stronie głównej!")
    time.sleep(2)
    for i in range(5):
        st.warning("Przekierowujemy cię na stronę główną za " + str(5 - i) + " sekund")
        time.sleep(1)
    st.switch_page("homePage.py")
