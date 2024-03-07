import streamlit as st
from streamlit_autorefresh import st_autorefresh
from st_pages import Page, show_pages, add_page_title


refresh_count = st_autorefresh(interval=10 * 60 * 1000, key="mainrefresh", limit=None)

# Optional -- adds the title and icon to the current page
add_page_title()
def run():
    show_pages(
        [
            Page("./pages/Estoque.py", "Estoque", "📦"),
            Page("./pages/Laboratorio.py", "Laboratorio", "👓"),       
        ]
    )
    page_name = st.sidebar.radio("Navegação", list(show_pages.keys()))
    show_pages[page_name]()

run()
