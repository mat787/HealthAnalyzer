import neurokit2 as nk
import pandas as pd

# Parametry techniczne pomiaru z zegarka apple watch
sampling_rate = 512  # Hz
PAPER_SPEED = 25     # mm/s
AMPLITUDE_SCALE = 10 # mm/mV

# 1. Wczytujemy dane i od razu nadajemy im nazwy kolumn
ekg_data = pd.read_csv("ekg.csv", skiprows=12, names=['sample', 'voltage'])

cleaned = nk.ecg_clean(ekg_data['voltage'], sampling_rate=sampling_rate)
print(cleaned)
signals, info = nk.ecg_process(ekg_data['voltage'], sampling_rate=sampling_rate)
nk.ecg_plot(signals, info)

print(ekg_data.head(20))

signal, waves = nk.ecg_delineate(cleaned, info, sampling_rate=sampling_rate, method="dwt", show=True, show_type='all')

import matplotlib.pyplot as plt
plt.show()






