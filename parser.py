from lxml import etree as ET
import pandas as pd

# input_file = 'test.xml'  #plik do testow parsera

def load_one_type(file_path, tag_name, type_name=None):
    """
    Pobiera dane na podstawie samego tagu (np. 'ActivitySummary') lub tagu i typu (np. 'Record' + 'hr').
    Chirurgiczna pęseta do eksploracji danych.
    """
    health_data = []

    if file_path is None:
        return "Zła ścieżka pliku"

    context = ET.iterparse(file_path, events=("end",))

    for event, elem in context:
        if elem.tag == tag_name:
            current_type = elem.get('type') or elem.get('workoutActivityType')
            if type_name is None or current_type == type_name:
                record = dict(elem.attrib)
                for child in elem:
                    if child.tag == "MetadataEntry":
                        record[child.get('key')] = child.get('value')
                health_data.append(record)

        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    if health_data:
        df = pd.DataFrame(health_data)
        if 'value' in df.columns:
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
        for date_col in ['startDate', 'endDate', 'creationDate']:
            if date_col in df.columns:
                df[date_col] = pd.to_datetime(df[date_col])
        return df
    return pd.DataFrame()

def load_all_health_data(file_path, mapping):
    """
    Wczytuje dane i grupuje je w DUŻE tabele według tagów (Record, Workout, ActivitySummary).
    Zamiast 50 małych tabel, otrzymasz kilka zbiorczych, co jest lepsze dla bazy SQL.
    """
    if file_path is None:
        return "Zła ścieżka pliku"
    if mapping is None:
        mapping = {}

    # 1. Inicjalizujemy kubełki na GŁÓWNE TAGI
    data_buckets = {
        "Record": [],
        "Workout": [],
        "ActivitySummary": []
    }

    context = ET.iterparse(file_path, events=("end",))

    for event, elem in context:
        tag = elem.tag
        if tag in data_buckets:
            long_type = elem.get('type') or elem.get('workoutActivityType') or tag
            if long_type in mapping or tag == "ActivitySummary":
                record = dict(elem.attrib)
                if long_type in mapping:
                    record['type'] = mapping[long_type]
                
                for child in elem:
                    if child.tag == "MetadataEntry":
                        record[child.get('key')] = child.get('value')
                data_buckets[tag].append(record)

        elem.clear()


    final_dfs = {}
    print("📊 Konwertuję dane na duże tabele zbiorcze...")

    for tag, records in data_buckets.items():
        if records:
            df = pd.DataFrame(records)
            if 'value' in df.columns:
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
            for date_col in ['startDate', 'endDate', 'creationDate']:
                if date_col in df.columns:
                    df[date_col] = pd.to_datetime(df[date_col])
            final_dfs[tag] = df

    print(f"✅ Wczytano {len(final_dfs)} dużych tabel!")
    return final_dfs




