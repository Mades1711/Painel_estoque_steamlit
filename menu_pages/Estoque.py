import streamlit as st
from datam import unique_cod_etapas, df_Etapas, df_Producao, df_OSAtrasadas


def app():

    
    st.title("Painel de produção")

    
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

    col1.bar_chart(
        df_Producao,
        x= 'Dia',
        y= 'QTD OS',
        width= 500,
        height= 450,
        color = ['#c4161c'],
        use_container_width = True
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
        width= 800,
        height= 400,
        )