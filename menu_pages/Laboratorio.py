import streamlit as st
from datam import  Os_Semana, OS_Dia, Os_Mes, Ag_montagem, df_OSAtrasadas


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
    font-size: 2.8em; 
    text-align: center;
    padding: 0px;
}

[data-testid="stMetric"] {
    margin-top: 2em;
    display: grid;
    place-items: center;
}
 
[data-testid="stMetricValue"] {
    font-size: 3.75em; 
}

[data-testid="stMetricDelta"]{
    font-size: 2.75em; 
}

[data-testid="stMetricLabel"]{   
    p{
        font-size: 2em; 
    }
}

.main .block-container {
    max-width: 95%;
        
}


[data-testid="stMetricDelta"] svg {
        display: none;
    }


[data-testid="stFullScreenFrame"]{
    display: grid;
    place-items: center;
    margin-top: 1.5em

   }


</style>
"""
def apply_css(css):
   st.markdown(css, unsafe_allow_html=True)

def app():
   
   apply_css(css)

   st.title("Painel de produção")


   col1, col2, col3, col4  = st.columns(4)

   col1.metric(label='OS do dia', value=OS_Dia, delta=None)
   col2.metric(label='OS da semana', value=Os_Semana, delta=None) 
   col3.metric(label='OS do mes', value=Os_Mes, delta=None)
   col4.metric(label='Aguardando montagem', value=Ag_montagem, delta=None)

   df_OSAt= df_OSAtrasadas[df_OSAtrasadas['COD_ETAPA']==2].drop(columns=['COD_ETAPA'])
   

   st.dataframe(
   data=df_OSAt,
   hide_index= True,
   column_config={
      "OS": st.column_config.NumberColumn(
            "OS",
            format="%d",
      ),
   },
   width= 900,
   height= 260,
   )
