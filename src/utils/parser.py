from lxml import etree as ET
import pandas as pd
import os


_TAGS = frozenset({"Record", "Workout", "ActivitySummary"})
_DATE_COLS = ["startDate", "endDate", "creationDate", "dateComponents"]


def load_all_health_data(file_path, mapping, progress_callback=None):
    if isinstance(file_path, str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Nie znaleziono pliku: {file_path}")
        file_obj = open(file_path, "rb")
        own_file = True
    else:
        file_obj, own_file = file_path, False
        file_obj.seek(0)

    file_obj.seek(0, 2)
    total_size = file_obj.tell()
    file_obj.seek(0)

    buckets     = {"Record": [], "Workout": [], "ActivitySummary": []}
    mapping_get = mapping.get
    last_pct    = -1

    try:
        for _, elem in ET.iterparse(file_obj, events=("end",)):
            tag = elem.tag
            if tag not in _TAGS:
                elem.clear()
                continue

            if progress_callback:
                pct = min(int(file_obj.tell() / total_size * 95), 95)
                if pct > last_pct:
                    progress_callback(pct)
                    last_pct = pct

            long_type = elem.get("type") or elem.get("workoutActivityType") or tag

            if tag != "ActivitySummary" and long_type not in mapping:
                elem.clear()
                continue

            record = dict(elem.attrib)
            if long_type in mapping:
                record["type"] = mapping_get(long_type)

            for child in elem:
                if child.tag == "MetadataEntry" and (key := child.get("key")):
                    record[key] = child.get("value")

            buckets[tag].append(record)
            elem.clear()
    finally:
        if own_file:
            file_obj.close()

    final_dfs = {}
    for i, (tag, records) in enumerate(buckets.items()):
        if not records:
            continue
        df = pd.DataFrame(records)
        df = df.loc[:, df.columns.notna()]
        if "value" in df.columns:
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
        for col in (c for c in _DATE_COLS if c in df.columns):
            df[col] = pd.to_datetime(df[col], errors="coerce")
        final_dfs[tag] = df
        if progress_callback:
            progress_callback(95 + int((i + 1) / len(buckets) * 5))

    if progress_callback:
        progress_callback(100)

    return final_dfs
