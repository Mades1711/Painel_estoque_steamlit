import streamlit as st
from datam import  Os_Semana, OS_Dia, Os_Mes, Ag_montagem, df_OSAtrasadas

def app():
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
   width= 800,
   height= 400,
   )
