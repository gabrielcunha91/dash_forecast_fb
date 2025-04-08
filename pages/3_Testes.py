import streamlit as st
import pandas as pd
import datetime
import calendar
from utils.functions.general_functions import *
from utils.queries import *
from workalendar.america import Brazil
from utils.functions.date_functions import *
from utils.functions.dash_forecast import *
from utils.components import *

st.set_page_config(
    page_title="Dash Forecast",
    page_icon="💰",
    layout="wide"
)

# # Seleção do período

# date_input = input_periodo_datas("periodo_datas_teste")
# start_date = pd.to_datetime(date_input[0])
# end_date = pd.to_datetime(date_input[1])
# start_date_year = start_date.year
# start_date_month = start_date.month
# end_date_year = end_date.year
# end_date_month = end_date.month
# df_projetado_e_zig = GET_DF_TICKET_BASE_E_ZIGPAY(start_date, end_date).fillna(0)

# df_ticket = df_projetado_e_zig.drop(columns=["Atendimentos_Base", "Atendimentos_Zig"])
# df_atendimentos = df_projetado_e_zig.drop(columns=["Ticket_Base", "Ticket_Zig"])

# st.dataframe(df_ticket, use_container_width=True, hide_index=True)
# st.divider()
# st.dataframe(df_atendimentos, use_container_width=True, hide_index=True)
# st.dataframe(df_calculo_faturamento(df_projetado_e_zig), use_container_width=True, hide_index=True)

# print(df_projetado_e_zig.dtypes)


df1 = {
    "Ticket_Base": [12, 18, 22, 28, 32],
    "Atendimentos_Base": [110, 160, 210, 260, 310],
    "Ticket_Zig": [10, 15, 20, 25, 30],
    "Atendimentos_Zig": [100, 150, 200, 250, 300]   
}

df2 = pd.DataFrame({
    "Data": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"],
    "Ticket_Base": [12, 18, 22, 28, 32],
    "Atendimentos_Base": [110, 160, 210, 260, 310],
    "Ticket_Zig": [10, 15, 0, 25, 0],
    "Atendimentos_Zig": [100, 150, 0, 250, 0]   
})

for i in df2.index[1:4]:
    print(i)