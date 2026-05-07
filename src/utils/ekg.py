import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import streamlit as st


def load_ecg(path, sampling_rate=512):
    try:
        df = pd.read_csv(path, sep=';', decimal=',', skiprows=12, header=None)
        ecg_raw = df.iloc[:, 0].values
    except FileNotFoundError:
        print("Nie znaleziono pliku")
        raise

    signals, info = nk.ecg_process(ecg_raw, sampling_rate=sampling_rate)
    nk.ecg_plot(signals, info)
    plt.gcf().set_size_inches(12, 8)

    return ecg_raw, signals, info, plt


def show_ecg(raw, clean, peaks, fs=512):
    t = np.arange(len(raw)) / fs

    fig = go.Figure()

    fig.add_trace(go.Scatter(
            x=t, y=raw,
            name='Surowy',
            line=dict(color='rgba(255, 255, 0, 0.4)', width=1)
        ))

    fig.add_trace(go.Scatter(
            x=t, y=clean,
            name='Czysty',
            line=dict(color='red', width=1.5)
        ))

    fig.add_trace(go.Scatter(
            x=t[peaks], y=clean[peaks],
            name='R-Peaks',
            mode='markers',
            marker=dict(color='white', symbol='triangle-down', size=10)
        ))

    fig.update_layout(
            title="Interaktywna analiza EKG",
            xaxis_title="Czas [s]",
            yaxis_title="Amplituda",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            template="plotly_dark",
            xaxis=dict(
                rangeslider=dict(visible=True),
                type="linear"
            )
        )

    st.plotly_chart(fig, width="stretch")






