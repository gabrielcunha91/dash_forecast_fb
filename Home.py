import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import os
import numpy as np
from utils.queries import *
from utils.user import *
from utils.functions.general_functions import *
from utils.functions.zigpay_api import *
# from workalendar.america import Brazil
# import openpyxl

def handle_login(userName, userPassoword):
    users = st.secrets["users"]

    if userName not in users['emails']:
        st.error("Usuário sem permissão.")
        return
    
    if user_data := login(userName, userPassoword):
        st.session_state["loggedIn"] = True
        st.session_state["user_data"] = user_data
    else:
        st.session_state["loggedIn"] = False
        st.error("Email ou senha inválidos!")

def show_login_page():
    st.markdown(""" 
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
                display: none;
                }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4,1])
    col1.write("## Dashboard - Forecast")
    userName = st.text_input(label="User name", value="", placeholder="Login", label_visibility="collapsed")
    userPassword = st.text_input(label="Password", value="", placeholder="Senha",type="password", label_visibility="collapsed")
    st.button("Login", on_click=handle_login, args=(userName, userPassword))

def get_casas():
    result, column_names = execute_query(GET_CASAS)
    df = pd.DataFrame(result, columns=column_names)
    return df

@st.cache_data
def get_casas_validas():
    result, column_names = execute_query(GET_CASAS)
    df_casas = pd.DataFrame(result, columns=column_names)
    lista_casas_validas = ['Abaru - Priceless', 'Arcos', 'Bar Brahma - Centro', 'Bar Brahma - Granja', 'Bar Léo - Centro', 'Blue Note - São Paulo', 'Blue Note SP (Novo)', 'Edificio Rolim', 'Girondino ', 'Girondino - CCBB', 'Jacaré', 'Love Cabaret', 'Notiê - Priceless', 'Orfeu', 'Priceless', 'Riviera Bar', 'Ultra Evil Premium Ltda ','Delivery Bar Leo Centro', 'Delivery Fabrica de Bares', 'Delivery Jacaré', 'Delivery Orfeu']
    df_validas = pd.DataFrame(lista_casas_validas, columns=["Casa"])
    df = df_casas.merge(df_validas, on="Casa", how="inner")
    return df

def get_orcamentos():
    result, column_names = execute_query(GET_ORCAMENTO)
    df_orcamentos = pd.DataFrame(result, columns=column_names)
    return df_orcamentos


def run():

    # Pagina Home
    st.write("# Dash Forecast")
    st.markdown(
        """
        Utilize as abas localizadas no lado esquerdo para buscar suas análises.
    """
    )
    
    # Puxando dados
    df_casas = get_casas_validas()
    if "df_casas" not in st.session_state:
        st.session_state["df_casas"] = df_casas
    
    df_orcamentos = get_orcamentos()
    if "df_orcamentos" not in st.session_state:
        st.session_state["df_orcamentos"] = df_orcamentos

    df_atendimentos = get_num_atendimentos_zigpay("2025-01-01", "2025-02-01", "0c3c7f44-d55b-497f-bce1-6367c535f368")
    if "df_atendimentos" not in st.session_state:
        st.session_state["dict_atendimentos"] = df_atendimentos
                                               

if __name__ == "__main__":
    
    # Configs da página
    st.set_page_config(
    page_title="Dash Forecast",
    page_icon="💰",
    layout="wide"
    )
    
    with st.sidebar:
        st.button(label="Logout", on_click=logout)

    if "loggedIn" not in st.session_state:
        st.session_state["loggedIn"] = False
        st.session_state["user_date"] = None

    if not st.session_state["loggedIn"]:
        show_login_page()
        st.stop()
    else:
        run()


