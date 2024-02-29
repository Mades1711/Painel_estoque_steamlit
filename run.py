import streamlit as st
import time
from streamlit_option_menu import option_menu
from menu_pages import Estoque, Laboratorio

# st.set_page_config(
#     page_title="Painel de produção",
#     layout="wide",
#     page_icon= "Logo_DI.png"
# )




class Multiapp:
    
    def __init__(self):
        self.apps = []
    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })
    def run():
        
        with st.sidebar: 
            app = option_menu(
                menu_title='Paineis',
                options=['Estoque', 'Laboratorio'],
                default_index= 0,
            )
        if app == 'Estoque':            
            Estoque.app()
        if app == 'Laboratorio':
            Laboratorio.app()
    run()
