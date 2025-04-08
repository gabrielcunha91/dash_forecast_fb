import streamlit as st
import pandas as pd
import datetime
from workalendar.america import Brazil
from utils.components import *
from utils.functions.date_functions import *
from utils.functions.general_functions import *
from utils.functions.dash_forecast import *
from utils.queries import *


st.set_page_config(
    page_title="Dash Forecast",
    page_icon="💰",
    layout="wide"
)

if 'loggedIn' not in st.session_state or not st.session_state['loggedIn']:
  st.switch_page('Home.py')

st.title("Dash Forecast")

# Seleção do período
date_input = input_periodo_datas("periodo_datas_pag_2")

# Seleção da casa
id_casa, casa = input_selecao_casas("input_casa_pag_2")


if len(date_input) == 2 and id_casa:

    # Convertendo as datas do "date_input" para datetime
    start_date = pd.to_datetime(date_input[0])
    end_date = pd.to_datetime(date_input[1])
    start_date_year = start_date.year
    start_date_month = start_date.month
    end_date_year = end_date.year
    end_date_month = end_date.month

    # Obtém dataframe principal
    df_projetado_e_zig = GET_DF_TICKET_BASE_E_ZIGPAY(start_date, end_date)

    # Substitui valores None por 0
    df_projetado_e_zig = df_projetado_e_zig.fillna(0)

    # Formata tipo de dados (int e float)
    df_projetado_e_zig['Ticket_Base'] = df_projetado_e_zig['Ticket_Base'].astype(float)
    df_projetado_e_zig['Atendimentos_Base'] = df_projetado_e_zig['Atendimentos_Base'].astype(int)
    df_projetado_e_zig['Ticket_Zig'] = df_projetado_e_zig['Ticket_Zig'].astype(float)
    df_projetado_e_zig['Atendimentos_Zig'] = df_projetado_e_zig['Atendimentos_Zig'].astype(int)
    
    # Filtrando dataframe pela casa
    df_projetado_e_zig = df_filtrar_casa(df_projetado_e_zig, id_casa)



    tab1, tab2, tab3 = st.tabs(["Ticket Médio", "Atendimentos", "Faturamento"])
    with tab1:
        st.header("Ticket Médio")
        df_ticket = df_estimativa_ticket(df_projetado_e_zig)
        st.dataframe(df_ticket, use_container_width=True, hide_index=True)
    with tab2:
        st.header("Atendimentos")
        df_atendimentos = df_estimativa_atendimentos(df_projetado_e_zig)
        st.dataframe(df_atendimentos, use_container_width=True, hide_index=True)
    with tab3:
        st.header("Faturamento")
        df_faturamento = df_calculo_faturamento(df_projetado_e_zig)
        st.dataframe(df_faturamento, use_container_width=True, hide_index=True)

else:
    st.warning("Selecione um período válido.")
    st.stop()


st.divider()





### Definindo Bases ##


# # st.subheader("Orcamentos")
# df_orcamentos = st.session_state["df_orcamentos"]
# df_orcamentos_filtrado = df_orcamentos[df_orcamentos['ID_Casa'] == id_casa]
# df_orcamentos_filtrado = df_orcamentos_filtrado[['Casa', 'Class_1', 'Class_2', 'Mes_Ref', 'Ano_Ref', 'Orcamento']]
# df_orcamentos_filtrado = format_columns_brazilian(df_orcamentos_filtrado, ['Orcamento'])
# df_orcamentos_filtrado = df_orcamentos_filtrado[(df_orcamentos_filtrado['Ano_Ref'] >= start_date_year) & (df_orcamentos_filtrado['Ano_Ref'] <= end_date_year)]
# df_orcamentos_filtrado = df_orcamentos_filtrado[(df_orcamentos_filtrado['Mes_Ref'] >= start_date_month) & (df_orcamentos_filtrado['Mes_Ref'] <= end_date_month)]


# st.dataframe(df_orcamentos_filtrado, 
#              use_container_width=True, hide_index=True)

# st.divider()