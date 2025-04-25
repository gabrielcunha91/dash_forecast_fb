import requests
import pymysql
import pandas as pd
import streamlit as st
from utils.functions.general_functions import *
from utils.functions.date_functions import *

def get_checkins(data_inicio, data_fim, id_zigpay):

    headers = {
            'Authorization': f'{st.secrets["zigpay_api"]["api_key"]}'
        }  

    url = "https://api.zigcore.com.br/integration/erp/checkins"

    # Inicializa pagina
    page = 1
    num_checkins = 0

    df = pd.DataFrame()

    while True:
                        
        params = {          
            "desde": f"{formata_data_sem_horario(data_inicio)}",
            "dtfim": f"{formata_data_sem_horario(data_fim)}",
            "loja": f"{id_zigpay}",
            "page": page   
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            checkins = response.json()

            df_page = pd.DataFrame(checkins)
            df = pd.concat([df, df_page])

            num_checkins += len(checkins)
            if len(checkins) < 50:
                break

            page += 1

        else:
            print(f"Erro {response.status_code} na requisição de check-ins.")
            print(response.text)
            break

    return num_checkins


# No futuro, adicionar get query para pegar os dados da T_TICKET_CLIENTES e adicionar no session state
@st.cache_data
def get_num_atendimentos_zigpay(start_date, end_date, id_zigpay):

    df_casas = st.session_state["df_casas"]

    # Mapeia ID_Zigpay para ID_Casa
    mapeamento_ids = dict(zip(df_casas["ID_Zigpay"], df_casas["ID_Casa"]))

    dados = []
    for data in pd.date_range(start_date, end_date, freq='D', inclusive='both'):
        # Verifica se o ID_Zigpay é válido
        if id_zigpay is None or not is_valid_uuid(id_zigpay):
            continue
        num_checkins = get_checkins(data, data, id_zigpay)
        if num_checkins is None:
            continue
        id_casa = mapeamento_ids[id_zigpay]
        dados.append({
            'ID_Casa': id_casa,
            'Data': data,
            'Num_Checkins': num_checkins
        })

    df = pd.DataFrame(dados)
    return df