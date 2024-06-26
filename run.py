from st_pages import Page, show_pages
import streamlit as st
def run():
    show_pages(
        [
            Page("./pages/Estoque.py", "Estoque", "📦"),
            Page("./pages/Laboratorio.py", "Laboratorio", "👓"),       
        ]
    )
    st.rerun()
run()