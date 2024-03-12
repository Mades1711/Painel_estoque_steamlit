import streamlit as st
import altair as alt
from datam import consulta, agrupamento_etapa, OS_atrasadas, OS_Produzidas
import datetime as dt
from streamlit_autorefresh import st_autorefresh


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

st.set_page_config(
        page_title="Painel de produção Estoque",
        page_icon= "Logo_DI.png",
        initial_sidebar_state='collapsed'
    )

def app():
    refresh_count = st_autorefresh(interval=10 * 60 * 1000, key="mainrefresh", limit=None)
    


    #Manipulação temporal
    today = dt.datetime.today()
    max_dt = today.date()
    first_day_month = (today.replace(day=1)).date()
    days_pass = (today - dt.timedelta(days=31) )
    print('atualizado', today)
    #consultas
    df= consulta()
    df_Etapas = agrupamento_etapa(df,first_day_month,today,max_dt)
    df_OSAtrasadas = OS_atrasadas(df)
    df_Producao = OS_Produzidas(df,days_pass,today)

    #variaveis
    unique_cod_etapas = df_Etapas['COD_ETAPA'].unique()

    apply_css(css)
    st.title("Painel de produção")
    
    # Definindo o número de métricas (colunas) por linha
    metrics_first_row = 5
    metrics_subsequent_row = 3

    # Total de itens para iterar
    total_items = len(unique_cod_etapas)

    # Inicializando o contador de linhas
    row_counter = 0

    i = 0
    while i < total_items:
        if row_counter == 0:
            # Primeira linha
            metrics_per_row = metrics_first_row
        else:
            # Linhas subsequentes
            metrics_per_row = metrics_subsequent_row

        cols = st.columns(metrics_per_row)
        
        for j in range(metrics_per_row):
            if i < total_items:
                cod_etapa = unique_cod_etapas[i]
                nome_etapa = df_Etapas.loc[df_Etapas['COD_ETAPA'] == cod_etapa, 'ETAPA'].iloc[0]
                valor_etapa = df_Etapas.loc[df_Etapas['COD_ETAPA'] == cod_etapa, 'LOJA'].iloc[0]
                valor_today = df_Etapas.loc[df_Etapas['COD_ETAPA'] == cod_etapa, 'Mov_at'].iloc[0]
                
                cols[j].metric(label=nome_etapa, value=valor_today, delta=valor_etapa, delta_color="off")
                
                i += 1

        row_counter += 1

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
    
app()