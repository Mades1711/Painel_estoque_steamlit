import streamlit as st
import fdb
import pandas as pd 
import warnings
from decouple import config
import datetime as dt
from consultas_sql import Mov_dia
from streamlit_autorefresh import st_autorefresh

warnings.filterwarnings('ignore')

#Manipulação temporal
today = dt.datetime.today()
max_dt = today.date()
next_month = today.replace(day=28) + dt.timedelta(days=4)
first_day_month = (today.replace(day=1))
final_month = (next_month - dt.timedelta(days=next_month.day))

start_of_week = today - dt.timedelta(days=today.weekday())

week_days = [start_of_week + dt.timedelta(days=i) for i in range(7)]

days_only = [day.strftime('%d') for day in week_days]
day_today = max_dt.strftime('%d')



def Connect():
  conn =fdb.connect(
      host=config('host'), 
      database=config('database'),
      user=config('user'), 
      password=config('password')
    )

  return conn

st_autorefresh(interval=120000, key="f5")
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
    df = df.drop(columns=['Hoje'])#'COD_ETAPA',

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

df_OSAtrasadas = OS_atrasadas() 
df_Producao = OS_Produzidas()
df_Etapas = agrupamento_etapa()




unique_cod_etapas = df_Etapas['COD_ETAPA'].unique()


Os_Semana = df_Producao[df_Producao['Dia'].isin(days_only)]['QTD OS'].sum()
OS_Dia = df_Producao[df_Producao['Dia']==day_today]['QTD OS'].sum()
Os_Mes = df_Producao['QTD OS'].sum()
Ag_montagem = df_Etapas[df_Etapas['COD_ETAPA']==16]['LOJA'].sum()




