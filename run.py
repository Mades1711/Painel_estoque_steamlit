import streamlit as st
from streamlit_option_menu import option_menu
from menu_pages import Estoque, Laboratorio

# st.set_page_config(
#     page_title="Painel de produção",
#     layout="wide",
#     page_icon= "Logo_DI.png"
# )

css = """
<style>
* {
margin: 0;  
padding: 0px;

}
.block-container { 
    display: block;
    justify-content: center;
    padding: 0px;
    }

[data-testid="StyledLinkIconContainer"]{
    font-size: 3em; 
    #margin-left: 0.5em;
    text-align: center;
    font-family: 'Segoe UI';
    color: #FFFFFF;
    padding: 0px;
}

# [data-testid="stHorizontalBlock"]{  
#     display: flex;
#     align-items: center; /* Centraliza verticalmente */
#     justify-content: center; /* Centraliza horizontalmente */
    
#   }
  
[data-testid="stMetricValue"] {
    font-size: 2.75em; 
}

[data-testid="stMetricDelta"]{
    font-size: 1.75em; 
}

[data-testid="stMetricLabel"]{   
    p{
        font-size: 0.25em; 
    }
}

.main .block-container {
    max-width: 95%;
        
}

[data-testid="stMetricLabel"] {
    font-size: 100px;
}

[data-testid="stMetricDelta"] svg {
        display: none;
    }

</style>
"""

def apply_custom_css(css):
    st.markdown(css, unsafe_allow_html=True)

class Multiapp:
    apply_custom_css(css)
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
