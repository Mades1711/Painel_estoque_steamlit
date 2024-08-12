import streamlit as st
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

st.set_page_config(
        page_title="Painel de produção Laboratório",
        page_icon= "Logo_DI.png",
        initial_sidebar_state='collapsed'
    )


def app():
    refresh_count = st_autorefresh(interval=10 * 60 * 1000, key="mainrefresh", limit=None) 
    #configuração da pagina

    #aplicando o css
    apply_css(css)
    st.title("Painel de produção")
    #Variaveis tempo
    
    today = dt.datetime.today()
    max_dt = today.date()
    first_day_month = (today.replace(day=1)).date()
    days_pass = (today - dt.timedelta(days=31) )

    start_of_week = today - dt.timedelta(days=today.weekday())
    week_days = [start_of_week + dt.timedelta(days=i) for i in range(7)]

    days_only = [day.strftime('%b %d') for day in week_days]
    day_today = max_dt.strftime('%b %d')


    #Puxando os dados
    df= consulta()
    df_Etapas = agrupamento_etapa(df,first_day_month,today,max_dt)
    df_OSAtrasadas = OS_atrasadas(df)
    df_Producao = OS_Produzidas(df,days_pass,today)

    #Metricas de etapas especificas
    Os_Semana = df_Producao[df_Producao['Dia'].isin(days_only)]['QTD OS'].sum()
    OS_Dia = df_Producao[df_Producao['Dia']==day_today]['QTD OS'].sum()
    Os_Mes = df_Etapas.loc[df_Etapas['COD_ETAPA'] == 30, 'LOJA'].iloc[0]
    Ag_montagem = df_Etapas[df_Etapas['COD_ETAPA']==15]['LOJA'].sum()
    Ag_montagems = df_Etapas[df_Etapas['COD_ETAPA']==5]['Mov_at'].sum()

    col1, col2, col3, col4  = st.columns(4)

    col1.metric(label='OS do dia', value=OS_Dia, delta=None)
    col2.metric(label='OS da semana', value=Os_Semana, delta=None) 
    col3.metric(label='OS do mes', value=Os_Mes, delta=None)
    col4.metric(label='Aguardando montagem', value=Ag_montagems, delta= Ag_montagem, delta_color="off")

    #Tabela puxando tudo que esteja 'Em montagem'
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
    
    

app()