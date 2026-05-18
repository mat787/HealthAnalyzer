# Apple Health Analyzer

Profesjonalna aplikacja analityczna do przetwarzania, wizualizacji oraz wykrywania anomalii w danych fizjologicznych pochodzących z ekosystemu Apple (iPhone & Apple Watch). Projekt demonstruje pełen pipeline ETL (Extract, Transform, Load) oraz implementację modeli uczenia maszynowego na rzeczywistych, "zaszumionych" danych z urządzeń wearables.

##  Kluczowe cechy
- **Algorytm Isolation Forest**: Wykorzystanie nienadzorowanego modelu uczenia maszynowego do detekcji nienaturalnych zachowań organizmu (np. tachykardii spoczynkowej).
- **Zaawansowany pipeline ETL**: Zoptymalizowane parsowanie złożonych struktur XML oraz proporcjonalna dystrybucja skumulowanych pakietów danych w czasie (rozbijanie pomiarów).
- **Wygładzanie fizjologiczne**: Wdrożenie techniki średniej ruchomej (Rolling Average) do modelowania "długu fizjologicznego", co drastycznie redukuje liczbę fałszywych alarmów (False Positives).
- **Standaryzacja stref czasowych**: Automatyczna konwersja logów systemowych do formatu UTC, zapewniająca spójność analityczną przy zmianach stref oraz czasu letniego/zimowego.
- **Interaktywny Dashboard**: Zbudowany w oparciu o architekturę Streamlit, pozwalający na dynamiczną eksplorację danych.

##  Technologie
- **Język**: Python 3.9+
- **Przetwarzanie Danych**: Pandas, NumPy
- **Machine Learning**: Scikit-Learn (Isolation Forest, StandardScaler)
- **Wizualizacja & Interfejs**: Streamlit

##  Wygląd aplikacji
<img width="1919" height="952" alt="img" src="https://github.com/user-attachments/assets/c2fc74ce-88fa-4fe7-97f1-b0f8a012bdb2" />
<img width="1918" height="948" alt="img_1" src="https://github.com/user-attachments/assets/91b2a492-0f6a-45e2-b3c6-9a5bb7087863" />
<img width="1919" height="950" alt="img_2" src="https://github.com/user-attachments/assets/23511408-a22c-4e4b-836d-1a5df522963f" />
<img width="1920" height="943" alt="img_3" src="https://github.com/user-attachments/assets/eccf1dd0-32ab-4a89-b197-5f73d9125067" />


##  Instalacja i uruchomienie
Aby zbudować środowisko i uruchomić aplikację lokalnie, należy wykonać poniższe komendy w terminalu:

```bash
git clone [https://github.com/TwojLogin/AppleHealthAnalyzer.git](https://github.com/TwojLogin/AppleHealthAnalyzer.git)
cd AppleHealthAnalyzer
pip install -r requirements.txt
streamlit run app.py

