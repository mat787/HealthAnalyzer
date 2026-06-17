import os
import sqlite3
import sys
from pathlib import Path

from src.utils.variables import short_names
from src.utils.parser import load_all_health_data
from src.utils.utils import clean_data

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


XML_PATH = "../../eksport.xml"
DB_PATH = "health_data.db"


def write_tables_to_db(data_tables, db_path=DB_PATH):
    if not data_tables:
        print("Brak danych do zapisania do bazy.")
        return

    print(f" Rozpoczynam proces budowania bazy: {db_path}")
    conn = sqlite3.connect(db_path)

    for table_name, df in data_tables.items():
        t_name = table_name.lower()
        print(f"\n Przetwarzanie: {t_name}...")

        df.to_sql(f"raw_{t_name}", conn, if_exists='replace', index=False)
        print(f" Zapisano wersję RAW ({len(df)} rekordów)")

        # --- WERSJA CZYSTA (CLEAN) ---
        df_cleaned = clean_data(df, t_name)
        df_cleaned.to_sql(f"clean_{t_name}", conn, if_exists='replace', index=False)
        print(f"  ✨ Zapisano wersję CLEAN ({len(df_cleaned)} rekordów)")

    cursor = conn.cursor()
    for table_name in data_tables.keys():
        t_name = table_name.lower()
        try:
            cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{t_name}_date ON clean_{t_name}(startDate)")
        except:
            pass

    conn.commit()
    conn.close()
    print("\nBaza danych gotowa.\n")


def setup_database():

    data_tables = load_all_health_data(XML_PATH, short_names)
    write_tables_to_db(data_tables, DB_PATH)



def delete_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
