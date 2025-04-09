import streamlit as st
from streamlit.logger import get_logger
from utils.functions.general_functions import *
import pandas as pd
import mysql.connector

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


def execute_query(query):
    try:
        conn = mysql_connection_fb()
        cursor = conn.cursor()
        cursor.execute(query)

        # Obter nomes das colunas
        column_names = [col[0] for col in cursor.description]
  
        # Obter resultados
        result = cursor.fetchall()
  
        cursor.close()
        conn.close()  # Fechar a conexão
        return result, column_names
    except mysql.connector.Error as err:
        LOGGER.error(f"Erro ao executar query: {err}")
        return None, None


def dataframe_query(query):
  resultado, nomeColunas = execute_query(query)
  dataframe = pd.DataFrame(resultado, columns=nomeColunas)
  return dataframe



# GET_CASAS = """
# WITH empresas_normalizadas AS (
#   SELECT
#     CASE 
#       WHEN ID IN (161, 162) THEN 149
#       ELSE ID
#     END AS ID_Casa_Normalizada,
#     NOME_FANTASIA,
#     FK_GRUPO_EMPRESA
#   FROM T_EMPRESAS
# )
# SELECT
#   te.ID_Casa_Normalizada AS ID_Casa,
#   te2.NOME_FANTASIA AS Casa
# FROM empresas_normalizadas te
# LEFT JOIN T_EMPRESAS te2 ON te.ID_Casa_Normalizada = te2.ID
# WHERE te.FK_GRUPO_EMPRESA = 100
# GROUP BY te.ID_Casa_Normalizada, te2.NOME_FANTASIA
# ORDER BY te2.NOME_FANTASIA
# """

GET_CASAS = """
SELECT te.ID AS ID_Casa,
te.NOME_FANTASIA AS Casa
FROM T_EMPRESAS te
"""

GET_ORCAMENTO = """
SELECT 
to2.ID as 'Orcamento_ID',
to2.FK_EMPRESA as 'ID_Casa',
te.NOME_FANTASIA as 'Casa',
to2.FK_CLASSIFICACAO_1 as 'ID_Class_1',
tccg.DESCRICAO as 'Class_1',
to2.FK_CLASSIFICACAO_2 as 'ID_Class_2',
tccg2.DESCRICAO as 'Class_2',
to2.MES as 'Mes_Ref',
to2.ANO as 'Ano_Ref',
to2.VALOR as 'Orcamento'
FROM T_ORCAMENTOS to2
INNER JOIN T_EMPRESAS te ON (to2.FK_EMPRESA = te.ID)
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_1 tccg ON (to2.FK_CLASSIFICACAO_1 = tccg.ID)
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_2 tccg2  ON (to2.FK_CLASSIFICACAO_2 = tccg2.ID)
WHERE to2.IS_VALID = 1
AND to2.ANO >= 2025
ORDER BY to2.ANO, to2.MES, te.ID, to2.FK_CLASSIFICACAO_1, tccg2.DESCRICAO 
"""

## GET_FATURAMENTOS_BASE_E_ZIG - query principal
@st.cache_data
def GET_DF_TICKET_BASE_E_ZIGPAY(data_inicio, data_fim):
    query = f'''
    SELECT 
      tbfp.FK_EMPRESA AS 'Casa',
      tbfp.DATA_PROJECAO AS 'Data',
      tbfp.TICKET_MEDIO AS 'Ticket_Base',
      tbfp.NUM_CLIENTES AS 'Atendimentos_Base',
      tztc.TICKET_MEDIO AS 'Ticket_Zig',
      tztc.NUM_CLIENTES AS 'Atendimentos_Zig'
    FROM
      T_BASE_FATURAMENTO_PROJETADO tbfp 
      LEFT JOIN T_ZIG_TICKET_CLIENTES tztc ON tbfp.FK_EMPRESA = tztc.FK_EMPRESA AND tbfp.DATA_PROJECAO = tztc.DATA_VENDA
    WHERE
      cast(tbfp.DATA_PROJECAO  AS date) >= '{data_inicio}' AND
      cast(tbfp.DATA_PROJECAO  AS date) <= '{data_fim}'
    '''
    return dataframe_query(query)