import streamlit as st
import altair as alt
import time
import datetime
from datam import today,unique_cod_etapas, df_Etapas, df_Producao, df_OSAtrasadas, consulta
 
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
    font-size: 2.4em; 
    text-align: center;
    padding: 0px;
}

[data-testid="stMetric"] {
    display: grid;
    place-items: center;
}
  
[data-testid="stMetricValue"] {
    font-size: 2.3em; 
}

[data-testid="stMetricDelta"]{
    font-size: 1.35em; 
}

[data-testid="stMetricLabel"]{   
    p{
        font-size: 1.2em; 
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
   }


</style>
"""
def apply_css(css):
   st.markdown(css, unsafe_allow_html=True)

def app():
    
    apply_css(css)
    st.title("Painel de produção")

    st.write(today) 
    

    metrics_per_row = 5

    for i in range(0, len(unique_cod_etapas), metrics_per_row):

        cols = st.columns(metrics_per_row)
            
        for j in range(metrics_per_row):
            
            if i + j < len(unique_cod_etapas):
                
                cod_etapa = unique_cod_etapas[i + j]
                
                nome_etapa = df_Etapas.loc[df_Etapas['COD_ETAPA'] == cod_etapa, 'ETAPA'].iloc[0]
                valor_etapa = df_Etapas.loc[df_Etapas['COD_ETAPA'] == cod_etapa, 'LOJA'].iloc[0]
                valor_today = df_Etapas.loc[df_Etapas['COD_ETAPA'] == cod_etapa, 'Mov_at'].iloc[0]
                
                cols[j].metric(label=nome_etapa, value=valor_today, delta=valor_etapa, delta_color="off")

    col1,col2  = st.columns(2)

    col1.altair_chart(
        alt.Chart(df_Producao).mark_bar().encode(
            x=alt.X('Dia', sort=None, title="Dia"),
            y=alt.Y('QTD OS', title="QTD OS"),
            color=alt.Color('QTD OS', scale=alt.Scale(scheme='reds'),legend=None)
        ), 
        use_container_width=True,    
    )


    col2.dataframe(
        data=df_OSAtrasadas.drop(columns=['COD_ETAPA']),
        hide_index= True,
        column_config={
            "OS": st.column_config.NumberColumn(
                "OS",
                format="%d",
            ),
        },
        width= 850,
        height= 250,
        )