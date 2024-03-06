import streamlit as st
from streamlit_autorefresh import st_autorefresh
from st_pages import Page, show_pages, add_page_title


refresh_count = st_autorefresh(interval=10 * 60 * 1000, key="mainrefresh", limit=None)

# Optional -- adds the title and icon to the current page
add_page_title()

show_pages(
    [
        Page("./menu_pages/Estoque.py", "Estoque", "📦"),
        Page("./menu_pages/Laboratorio.py", "Laboratório", "👓"),       
    ]
)


