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
    
    df_casas = st.session_state["df_casas"]

    lista_casas_validas = ['Abaru - Priceless', 'Arcos', 'Bar Brahma - Centro', 'Bar Brahma - Granja', 'Bar Léo - Centro', 'Blue Note - São Paulo', 'Blue Note SP (Novo)', 'Edificio Rolim', 'Girondino ', 'Girondino - CCBB', 'Jacaré', 'Love Cabaret', 'Notiê - Priceless', 'Orfeu', 'Priceless', 'Riviera Bar', 'Ultra Evil Premium Ltda ','Delivery Bar Leo Centro', 'Delivery Fabrica de Bares', 'Delivery Jacaré', 'Delivery Orfeu']
    df_validas = pd.DataFrame(lista_casas_validas, columns=["Casa"])
    casa = st.selectbox("Casa", lista_casas_validas,key=key)

    df = df_casas.merge(df_validas, on="Casa", how="inner")
    # Definindo um dicionário para mapear nomes de casas a IDs de casas
    mapeamento_lojas = dict(zip(df["Casa"], df["ID_Casa"]))

    # Obtendo o ID da casa selecionada
    id_casa = mapeamento_lojas[casa]
    st.write('ID da casa selecionada:', id_casa)
    return id_casa, casa



    
