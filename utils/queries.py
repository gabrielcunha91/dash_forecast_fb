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


GET_CASAS = """
SELECT te.ID AS ID_Casa,
te.NOME_FANTASIA AS Casa,
te.ID_ZIGPAY AS ID_Zigpay
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
def GET_DF_TICKET_BASE_E_ZIGPAY():
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
    '''
    return dataframe_query(query)

# Dataframe com os valores e quantidades dos itens vendidos pela casa
@st.cache_data
def GET_DF_ITENS_VENDIDOS(id_casa):
    query = f'''
    SELECT 
      tiv.EVENT_DATE AS 'Data_Evento',
      te.NOME_FANTASIA AS 'Casa',
      tivc.NOME_PRODUTO AS 'Nome_Produto',
      tiv.UNIT_VALUE AS 'Valor_Unit',
      tiv.COUNT AS 'Qtde',
      tiv.DISCOUNT_VALUE AS 'Desconto',
      tivc2.DESCRICAO AS 'Categoria'
    FROM  
      T_ITENS_VENDIDOS tiv LEFT JOIN
      T_EMPRESAS te ON tiv.LOJA_ID = te.ID_ZIGPAY LEFT JOIN
      T_ITENS_VENDIDOS_CADASTROS tivc ON tiv.PRODUCT_ID = tivc.ID_ZIGPAY LEFT JOIN
      T_ITENS_VENDIDOS_CATEGORIAS tivc2 ON tivc.FK_CATEGORIA = tivc2.ID
    WHERE
      te.ID = {id_casa}
    '''
    return dataframe_query(query)