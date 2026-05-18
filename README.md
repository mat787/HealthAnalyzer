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


##  Instalacja i uruchomienie
Aby zbudować środowisko i uruchomić aplikację lokalnie, należy wykonać poniższe komendy w terminalu:

```bash
git clone [https://github.com/TwojLogin/AppleHealthAnalyzer.git](https://github.com/TwojLogin/AppleHealthAnalyzer.git)
cd AppleHealthAnalyzer
pip install -r requirements.txt
streamlit run app.py

