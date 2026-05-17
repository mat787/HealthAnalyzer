import time
from io import BytesIO

import streamlit as st
from src.utils.parser import load_all_health_data
from src.database.setup_db import short_names, write_tables_to_db, delete_db

st.set_page_config(layout="wide")
st.title("Apple Health Analyzer")
st.header("Wstaw swój plik Apple Health poniżej")

if 'final_dfs' not in st.session_state:
    st.session_state["final_dfs"] = None
if st.session_state["final_dfs"] is None:

    plik = st.file_uploader("Wstaw plik", "xml", False)

    if plik is not None:
        plik.seek(0)

        st.write("Wczytuję dane, to może chwilkę potrwać...")

        progress_bar = st.progress(0)
        progress_status = st.empty()

        def progress_callback(progress):
            progress_bar.progress(progress)
            progress_status.text(f"Postęp: {progress}%")

        file_buffer = BytesIO(plik.getbuffer())

        final_dfs = load_all_health_data(file_buffer, short_names, progress_callback)

        progress_bar.progress(100)
        progress_status.text("Gotowe!")
        st.session_state["final_dfs"] = final_dfs
        time.sleep(2)
        st.rerun()
else:
        st.success("Plik został pomyślnie przetworzony i znajduje się w pamięci!")
        if st.button("Przejdź do analizy (Dashboard)"):
            st.switch_page("pages/goalPage.py")
        # Przycisk do zapisu w bazie (pojawia się dopiero, jak mamy dane)
        if st.button('Zapisz dane do lokalnej bazy danych'):
            final_dfs = st.session_state["final_dfs"]
            write_tables_to_db(final_dfs)
            st.success("Dane zostały pomyślnie zapisane w lokalnej bazie danych!")



        if st.button("Zresetuj dane"):
            st.session_state["final_dfs"] = None
            st.rerun()
        if st.button("Usuń dane z bazy"):
            delete_db()