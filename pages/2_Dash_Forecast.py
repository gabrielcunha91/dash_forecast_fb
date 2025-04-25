import streamlit as st
import pandas as pd
import datetime
from workalendar.america import Brazil
from utils.components import *
from utils.functions.date_functions import *
from utils.functions.general_functions import *
from utils.functions.dash_forecast import *
from utils.queries import *
from utils.functions.zigpay_api import *
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

st.set_page_config(
    page_title="Dash Forecast",
    page_icon="💰",
    layout="wide",
)

if 'loggedIn' not in st.session_state or not st.session_state['loggedIn']:
  st.switch_page('Home.py')

st.title("Dash Forecast")

# Seleção do período
date_input = input_periodo_datas("periodo_datas_pag_2")

# Seleção da casa
id_casa, casa, id_zigpay = input_selecao_casas("input_casa_pag_2")


if len(date_input) == 2 and id_casa:

    # Convertendo as datas do "date_input" para datetime
    start_date = pd.to_datetime(date_input[0])
    end_date = pd.to_datetime(date_input[1])
    start_date_year = start_date.year
    start_date_month = start_date.month
    end_date_year = end_date.year
    end_date_month = end_date.month

    # Obtém dataframe principal
    df_projetado_e_zig = GET_DF_TICKET_BASE_E_ZIGPAY()

    # Adiciona coluna Num_Checkins da API
    df_atendimentos = get_num_atendimentos_zigpay("2025-01-01", formata_data_sem_horario(get_today()), id_zigpay)
    df_projetado_e_zig = pd.merge(df_projetado_e_zig, df_atendimentos, on='Data', how='left')
   
    # Adiciona coluna Faturamento_Liquido da API
    df_faturamentos_zig = df_faturamento_por_dia(id_casa)
    df_faturamentos_zig = df_formata_data_horario_zero(df_faturamentos_zig, 'Data_Evento')
    df_faturamentos_zig['Data_Evento'] = pd.to_datetime(df_faturamentos_zig['Data_Evento'])
    df_projetado_e_zig = pd.merge(df_projetado_e_zig, df_faturamentos_zig, right_on='Data_Evento', left_on='Data', how='left')
    
    # Calcula Ticket Médio com base em Num_Checkins e Faturamento_Liquido
    df_faturamentos_zig = df_calculo_ticket_medio(df_projetado_e_zig, 'Valor_Liquido', 'Num_Checkins')

    # Substitui valores None por 0
    df_projetado_e_zig = df_projetado_e_zig.fillna(0)

    # Formata tipo de dados
    tipos_de_dados = {
        'Ticket_Base': float,
        'Atendimentos_Base': int,
        'Ticket_Zig': float,
        'Atendimentos_Zig': int
    }
    df_projetado_e_zig = df_projetado_e_zig.astype(tipos_de_dados, errors='ignore')

    # Filtrando dataframe pela casa
    df_projetado_e_zig = df_filtrar_casa(df_projetado_e_zig, id_casa)
    if df_projetado_e_zig.empty:
        st.warning("Selecione uma casa válida.")

    else:
        
        # Funções de estimativas
        df_estimativa_ticket_proximo_mes(df_projetado_e_zig)
        df_estimativa_atendimentos_proximo_mes(df_projetado_e_zig)
        df_calculo_faturamento(df_projetado_e_zig)

        # Filtra pela data selecionada
        df_projetado_e_zig = df_filtrar_periodo_data(df_projetado_e_zig, 'Data', start_date, end_date)
        
        # Formata a data para o formato brasileiro
        df_projetado_e_zig = df_format_date_brazilian(df_projetado_e_zig, 'Data')

        tab1, tab2, tab3 = st.tabs(["Ticket Médio", "Atendimentos", "Faturamento"])

        with tab1:
            st.header("Ticket Médio")
            if df_projetado_e_zig.empty:
                st.warning("Não há previsão para o período selecionado")
            else:
                format_columns_brazilian(df_projetado_e_zig, ['Ticket_Base', 'Ticket_Medio_Faturamento','Estimativa_Ticket'])
                st.dataframe(df_projetado_e_zig[['Data', 'Ticket_Base', 'Ticket_Medio_Faturamento', 'Estimativa_Ticket']], use_container_width=True, hide_index=True)
                
        with tab2:
            st.header("Atendimentos")
            if df_projetado_e_zig.empty:
                st.warning("Não há previsão para o período selecionado")
            else:
                st.dataframe(df_projetado_e_zig[['Data', 'Atendimentos_Base', 'Num_Checkins', 'Estimativa_Atendimentos']], use_container_width=True, hide_index=True)

        with tab3:
            st.header("Faturamento")
            if df_projetado_e_zig.empty:
                st.warning("Não há previsão para o período selecionado")
            else:
                format_columns_brazilian(df_projetado_e_zig, ['Faturamento_Base', 'Faturamento_Zigpay','Estimativa_Faturamento'])
                st.dataframe(df_projetado_e_zig[['Data', 'Faturamento_Base', 'Faturamento_Zigpay', 'Estimativa_Faturamento']], use_container_width=True, hide_index=True)

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