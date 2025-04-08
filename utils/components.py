import pandas as pd
import streamlit as st
from utils.functions.date_functions import *

def input_periodo_datas(key):
    today = get_today()
    jan_this_year = get_jan_this_year(today)
    first_day_this_month_this_year = get_first_day_this_month_this_year(today)
    last_day_this_month_this_year = get_last_day_this_month_this_year(today)

    # Inicializa o input com o mês atual
    date_input = st.date_input("Período",
                            value=(first_day_this_month_this_year, last_day_this_month_this_year),
                            min_value=jan_this_year,
                            format="DD/MM/YYYY",
                            key=key
                            )
    return date_input

def input_selecao_casas(key):
    # Filtrando casas
    df_casas = st.session_state["df_casas"] 
    casas = df_casas['Casa'].tolist()
    casa = st.selectbox("Casa", casas, key=key)
    # Definindo um dicionário para mapear nomes de casas a IDs de casas
    mapeamento_lojas = dict(zip(df_casas["Casa"], df_casas["ID_Casa"]))

    # Obtendo o ID da casa selecionada
    id_casa = mapeamento_lojas[casa]
    st.write('ID da casa selecionada:', id_casa)
    return id_casa, casa



    
