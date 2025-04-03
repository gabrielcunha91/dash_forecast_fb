import streamlit as st
import pandas as pd
import datetime
import streamlit as st
from utils.functions.date_functions import *
from utils.functions.general_functions import *
from utils.queries import *
from workalendar.america import Brazil

st.set_page_config(
    page_title="Dash Forecast",
    page_icon="💰",
    layout="wide"
)

st.title("Dash Forecast")

# Filtrando Data
today = get_today()
last_year = get_last_year(today)
jan_last_year = get_jan_last_year(last_year)
jan_this_year = get_jan_this_year(today)
last_day_of_month = get_last_day_of_month(today)
first_day_this_month_this_year = get_first_day_this_month_this_year(today)
last_day_this_month_this_year = get_last_day_this_month_this_year(today)
dec_this_year = get_dec_this_year(today)
start_of_three_months_ago = get_start_of_three_months_ago(today)

date_input = st.date_input("Período",
                           (first_day_this_month_this_year, last_day_this_month_this_year),
                           min_value=jan_this_year,
                           format="DD/MM/YYYY"
                           )

# Convertendo as datas do "date_input" para datetime
start_date = pd.to_datetime(date_input[0])
end_date = pd.to_datetime(date_input[1])

start_date_year = start_date.year
start_date_month = start_date.month
end_date_year = end_date.year
end_date_month = end_date.month

# Filtrando casas
df_casas = st.session_state["df_casas"]
casas = df_casas['Casa'].tolist()
casa = st.selectbox("Casa", casas)

# Definindo um dicionário para mapear nomes de casas a IDs de casas
mapeamento_lojas = dict(zip(df_casas["Casa"], df_casas["ID_Casa"]))

# Obtendo o ID da casa selecionada
id_casa = mapeamento_lojas[casa]
st.write('ID da casa selecionada:', id_casa)

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

tab1, tab2, tab3 = st.tabs(["Ticket Médio", "Atendimentos", "Faturamento"])

with tab1:
    st.header("Ticket Médio")
with tab2:
    st.header("Atendimentos")
with tab3:
    st.header("Faturamento")

