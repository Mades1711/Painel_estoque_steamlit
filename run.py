import streamlit as st
import fdb
import pandas as pd 
import numpy as np
from decouple import config
import datetime as dt
from consultas_sql import Mov_dia
import warnings

warnings.filterwarnings('ignore')

today = dt.datetime.today()
max_dt = today.date()
next_month = today.replace(day=28) + dt.timedelta(days=4)
first_day_month = (today.replace(day=1))#.strftime('%d/%m/%y')
final_month = (next_month - dt.timedelta(days=next_month.day))#.strftime('%d/%m/%y')

st.set_page_config(
    page_title="Painel de produção",
    layout="wide",
    page_icon= "Logo_DI.png"
)


def Connect():
  conn =fdb.connect(
      host=config('host'), 
      database=config('database'),
      user=config('user'), 
      password=config('password')
    )

  return conn

@st.cache_data
def consulta():
    df= pd.read_sql(Mov_dia, Connect())
    return df

def agrupamento_etapa():
    df= consulta()
    

    df_prod = df[df['COD_ETAPA']== 4] 
    df_prod['Ultima mov'] = pd.to_datetime(df_prod['Ultima mov'])   
    df_prod['Mov_at'] = max_dt
    df_prod['Mov_at'] = df_prod['Mov_at'] == df_prod['Ultima mov']
    df_prod = df_prod[df_prod['Ultima mov'].between(first_day_month, final_month)]
    #df_prod = df_prod[df_prod['Mov_at']==True]
    df_prod= df_prod.groupby(['COD_ETAPA','ETAPA']).agg({'LOJA':'count','Mov_at':'sum'}).reset_index()

    df = df[df['COD_ETAPA']!= 4] 
    df['Ultima mov'] = pd.to_datetime(df['Ultima mov'])
    df['Ultima mov'] = df['Ultima mov'].dt.date
    
    df['Mov_at'] = df['Ultima mov']== max_dt    
    df= df.groupby(['COD_ETAPA','ETAPA']).agg({'LOJA':'count','Mov_at':'sum'}).reset_index()   
    soma_OS = df['LOJA'].sum()
    soma_OS_td = df['Mov_at'].sum()

    df = pd.concat([df, df_prod], ignore_index= True) 
    df = df.query('COD_ETAPA in (1,2,3,4,10,15,16,13,12,20)')
    
    tota_prod = {'COD_ETAPA':30 ,'ETAPA':'OS em produção', 'LOJA': soma_OS, 'Mov_at' :soma_OS_td}
    df_tota_prod = pd.DataFrame([tota_prod])
    df = pd.concat([df,df_tota_prod], ignore_index= True)

    df['LOJA'] = df['LOJA'].astype(str)
    df['Mov_at'] = df['Mov_at'].astype(str)
    
    ordem_index = [1,10,2,3,12,15,16,20,13,4,30]
    df['Ordem'] = df['COD_ETAPA'].map(lambda x: ordem_index.index(x))
    df = df.sort_values('Ordem').drop('Ordem', axis=1)

    return df


def OS_atrasadas():
    df = consulta()
    #pegando tudo que nao é Translado laboratório -> loja
    df = df[df['COD_ETAPA']!= 4] 
    
    df['PREVISAO'] = pd.to_datetime(df['PREVISAO'])
    df['Ultima mov'] = pd.to_datetime(df['Ultima mov'])

    #separando OS sem data de previsão
    df_semdt = df.fillna({'PREVISAO': 'SEM DATA DE PREVISÃO'})
    df_semdt = df_semdt.query("PREVISAO == 'SEM DATA DE PREVISÃO'")  
    df_semdt['Ultima mov'] = df_semdt['Ultima mov'].dt.strftime('%d/%m/%y')

    #pegando tudo que está atrasado
    df = df.query("PREVISAO.notnull()")  
    df['Hoje'] = pd.to_datetime(max_dt)
    df['Dias Atrasados'] = (df['PREVISAO'] - df['Hoje'] ).dt.days    
    df = df[df['Dias Atrasados']<0] 
    df['Dias Atrasados'] = df['Dias Atrasados'].abs()
    df['PREVISAO']= df['PREVISAO'].dt.strftime('%d/%m/%y')
    df['Ultima mov']= df['Ultima mov'].dt.strftime('%d/%m/%y')
    df = df.sort_values(by = ['Dias Atrasados'], ascending= False )
    df = pd.concat([df,df_semdt])
    df = df.drop(columns=['COD_ETAPA','Hoje'])

    return df


def OS_Produzidas():    
    df = consulta() 
    #pegando tudo que é Translado laboratório -> loja
    df = df[df['COD_ETAPA']== 4]
    df = df.drop(columns=['PREVISAO','COD_ETAPA'])
    df['Ultima mov'] = pd.to_datetime(df['Ultima mov'])
    df = df[df['Ultima mov'].between(first_day_month, final_month)]    
    df['Ultima mov']= df['Ultima mov'].dt.strftime('%d')    
    df= df.groupby(['Ultima mov']).agg({'LOJA':'count'}).reset_index()
    df = df.rename(columns={'Ultima mov' : 'Dia', 'LOJA' : 'QTD OS'})

    return df


css = """
<style>
* {
  margin: 0;  
  padding: 0px;
  box-sizing: border-box;
  
}

[data-testid="StyledLinkIconContainer"]{
    font-size: 4.25em; 
    #margin-left: 0.5em;
    text-align: center;
    font-family: 'Segoe UI';
    color: #FFFFFF;
}

[data-testid="stMetric"]{
    margin-left: 4em;
    font-family: 'Segoe UI';
    color: #FFFFFF;
    
}

[data-testid="stMetricContainer"] {
    p{
        font-size: 2.75em !important;
    }
}

[data-testid="stMetricValue"] {
    font-size: 2.75em; 
}

[data-testid="stMetricDelta"]{
    font-size: 1.75em; 
}

[data-testid="stArrowVegaLiteChart"]{
    margin-left: 4em;
    width: 100px;
    height: 200px;
}

[data-testid="stDataFrame"]{
    margin-left: 4em;
}

.block-container { padding: 0px !important; }
</style>
"""

st.markdown(css, unsafe_allow_html=True)
st.title('Painel de produção')

metrics_per_row = 5

df_OSAtrasadas = OS_atrasadas() 
df_Producao = OS_Produzidas()
df_Etapas = agrupamento_etapa()

unique_cod_etapas = df_Etapas['COD_ETAPA'].unique()

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
col1.bar_chart(
    df_Producao,
    x= 'Dia',
    y= 'QTD OS',
    width= 500,
    height= 450,
    color = ['#c4161c']

    )

col2.dataframe(
    data=df_OSAtrasadas,
    hide_index= True,
    column_config={
        "OS": st.column_config.NumberColumn(
            "OS",
            format="%d",
        ),
    },
    
    )