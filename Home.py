import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import os
import numpy as np
from datetime import datetime
import mysql.connector
from utils.queries import *
from utils.user import *
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

LOGGER = get_logger(__name__)

def mysql_connection_fb():
  mysql_config = st.secrets["mysql_fb"]

  conn_fb = mysql.connector.connect(
        host=mysql_config['host'],
        port=mysql_config['port'],
        database=mysql_config['database'],
        user=mysql_config['username'],
        password=mysql_config['password']
    )    
  return conn_fb


def execute_query(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)

    # Obter nomes das colunas
    column_names = [col[0] for col in cursor.description]
  
    # Obter resultados
    result = cursor.fetchall()
  
    cursor.close()
    return result, column_names


def casas(connection):
    result, column_names = execute_query(GET_CASAS, connection)
    df_casas = pd.DataFrame(result, columns=column_names)
    return df_casas

def orcamentos(connection):
    result, column_names = execute_query(GET_ORCAMENTO, connection)
    df_orcamentos = pd.DataFrame(result, columns=column_names)
    return df_orcamentos


def run():

    # Puxando dados
    conn_fb = mysql_connection_fb()
    df_casas = casas(conn_fb)
    df_orcamentos = orcamentos(conn_fb)            

    # Pagina Home
    st.write("# Dash Forecast")
    st.markdown(
        """
        Utilize as abas localizadas no lado esquerdo para buscar suas análises.
    """
    ) 

    # Adiciona dataframes ao session_state do Streamlit
    if "df_casas" not in st.session_state:
        st.session_state["df_casas"] = df_casas
    if "df_orcamentos" not in st.session_state:
        st.session_state["df_orcamentos"] = df_orcamentos       
                                               

if __name__ == "__main__":
    
    # Configs da página
    st.set_page_config(
    page_title="Dash Forecast",
    page_icon="💰",
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


