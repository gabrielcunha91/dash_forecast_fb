import streamlit as st
import pandas as pd
import datetime
import calendar
from utils.functions.general_functions import *
from utils.queries import *
from workalendar.america import Brazil

st.set_page_config(
    page_title="Dash Forecast",
    page_icon="💰",
    layout="wide"
)


# Filtrando Data
today = datetime.datetime.now()
last_year = today.year - 1
jan_last_year = datetime.datetime(last_year, 1, 1)
jan_this_year = datetime.datetime(today.year, 1, 1)
last_day_of_month = calendar.monthrange(today.year, today.month)[1]
first_day_this_month_this_year = datetime.datetime(today.year, today.month, 1)
last_day_this_month_this_year = datetime.datetime(today.year, today.month, last_day_of_month)
dec_this_year = datetime.datetime(today.year, 12, 31)

## 3 meses atras
month_sub_3 = today.month - 3
year = today.year

if month_sub_3 <= 0:
    # Se o mês resultante for menor ou igual a 0, ajustamos o ano e corrigimos o mês
    month_sub_3 += 12
    year -= 1

start_of_three_months_ago = datetime.datetime(year, month_sub_3, 1)


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
st.subheader("Orcamentos")
df_orcamentos = st.session_state["df_orcamentos"]
df_orcamentos_filtrado = df_orcamentos[df_orcamentos['ID_Casa'] == id_casa]
df_orcamentos_filtrado = df_orcamentos_filtrado[['Casa', 'Class_1', 'Class_2', 'Mes_Ref', 'Ano_Ref', 'Orcamento']]
df_orcamentos_filtrado = format_columns_brazilian(df_orcamentos_filtrado, ['Orcamento'])
df_orcamentos_filtrado = df_orcamentos_filtrado[(df_orcamentos_filtrado['Ano_Ref'] >= start_date_year) & (df_orcamentos_filtrado['Ano_Ref'] <= end_date_year)]
df_orcamentos_filtrado = df_orcamentos_filtrado[(df_orcamentos_filtrado['Mes_Ref'] >= start_date_month) & (df_orcamentos_filtrado['Mes_Ref'] <= end_date_month)]


st.dataframe(df_orcamentos_filtrado, 
            #  column_config={
            #      "Casa"
            #  },
             use_container_width=True, hide_index=True)

st.divider()


