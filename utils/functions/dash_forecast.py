import streamlit as st
import pandas as pd
import datetime
from utils.queries import *
from utils.functions.date_functions import *
from utils.functions.general_functions import *


def idx_ultimo_dia_com_ticket_zig(df):
    indices_ticket_zig = df.loc[df['Ticket_Medio_Faturamento'] != 0].index

    if len(indices_ticket_zig) == 0:
        return None
    return max(indices_ticket_zig)

def idx_ultimo_dia_com_faturamento_liquido(df):
    indices_faturamento_liquido = df.loc[df['Valor_Liquido'] != 0].index

    if len(indices_faturamento_liquido) == 0:
        return None
    return max(indices_faturamento_liquido)


def idx_ontem(df):
    data_ontem = pd.to_datetime('today') - pd.Timedelta(days=1)
    data_ontem = data_ontem.strftime('%Y-%m-%d 00:00:00')
    indices_ontem = df.loc[df['Data'] == data_ontem].index
    return indices_ontem[0]

# Estimativa de Ticket para o primeiro mes
def df_estimativa_ticket_proximo_mes(df):

    # Ultimo dia com dados reais
    idx_ultimo_dia_zig = idx_ultimo_dia_com_faturamento_liquido(df)
    if idx_ultimo_dia_zig == None or idx_ultimo_dia_zig > df.index.max():
        return df
    ultimo_dia_zig = pd.to_datetime(df.loc[idx_ultimo_dia_zig, 'Data'])
    mes_ultimo_dia_zig = ultimo_dia_zig.month
    
    # Calcula o primeiro dia de estimativa
    idx_primeiro_dia_estimativa = idx_ultimo_dia_zig + 1
    if idx_primeiro_dia_estimativa > df.index.max():
        return df
    
    primeiro_dia = pd.to_datetime(df.loc[idx_primeiro_dia_estimativa, 'Data'])
    mes_primeiro_dia = primeiro_dia.month

    # Ultimo dia do mes
    ultimo_dia = get_last_day_of_month(primeiro_dia)
    num_estimativas = ultimo_dia - primeiro_dia.day
    idx_ultimo_dia_estimativa = idx_primeiro_dia_estimativa + num_estimativas

    if idx_ultimo_dia_zig != None and idx_primeiro_dia_estimativa in df.index and idx_ultimo_dia_estimativa in df.index:

        if mes_primeiro_dia != mes_ultimo_dia_zig:
            return df
        
        else:
            # Verifica se o dataframe já possui a coluna 'Estimativa_Ticket'.
            if not ('Estimativa_Ticket' in df.columns):
                df['Estimativa_Ticket'] = 0.0

            estimativas_semana = []

            for i in df.index[idx_primeiro_dia_estimativa:idx_ultimo_dia_estimativa + 1]:
                # Verifica se o dia é da primeira semana da estimativa
                if i in df.index[idx_primeiro_dia_estimativa:idx_primeiro_dia_estimativa + 7]:
                    estimativa_dia = (df.loc[i - 7, 'Ticket_Medio_Faturamento'] + df.loc[i - 14, 'Ticket_Medio_Faturamento']) / 2
                    df.loc[i, 'Estimativa_Ticket'] = estimativa_dia
                    estimativas_semana.insert(i % 7, estimativa_dia)
                # Proximas semanas do mês
                else:
                    df.loc[i, 'Estimativa_Ticket'] = estimativas_semana[i % 7]

    return df


# Dataframe das estimativas - Atendimentos (até 1 mês)
def df_estimativa_atendimentos_proximo_mes(df):

    # Ultimo dia com dados reais
    idx_ultimo_dia_zig = idx_ontem(df)
    if idx_ultimo_dia_zig == None or idx_ultimo_dia_zig > df.index.max():
        return df
    ultimo_dia_zig = pd.to_datetime(df.loc[idx_ultimo_dia_zig, 'Data'])
    mes_ultimo_dia_zig = ultimo_dia_zig.month
    
    # Calcula o primeiro dia de estimativa
    idx_primeiro_dia_estimativa = idx_ultimo_dia_zig + 1
    if idx_primeiro_dia_estimativa > df.index.max():
        return df
    
    primeiro_dia = pd.to_datetime(df.loc[idx_primeiro_dia_estimativa, 'Data'])
    mes_primeiro_dia = primeiro_dia.month

    # Ultimo dia do mes
    ultimo_dia = get_last_day_of_month(primeiro_dia)
    num_estimativas = ultimo_dia - primeiro_dia.day
    idx_ultimo_dia_estimativa = idx_primeiro_dia_estimativa + num_estimativas

    if idx_ultimo_dia_zig != None and idx_primeiro_dia_estimativa in df.index and idx_ultimo_dia_estimativa in df.index:

        if mes_primeiro_dia != mes_ultimo_dia_zig:
            return df
        
        else:
            # Verifica se o dataframe já possui a coluna 'Estimativa_Atendimentos'.
            if not ('Estimativa_Atendimentos' in df.columns):
                df['Estimativa_Atendimentos'] = 0

            estimativas_semana = []

            for i in df.index[idx_primeiro_dia_estimativa:idx_ultimo_dia_estimativa + 1]:
                # Verifica se o dia é da primeira semana da estimativa
                if i in df.index[idx_primeiro_dia_estimativa:idx_primeiro_dia_estimativa + 7]:
                    estimativa_dia = round((df.loc[i - 7, 'Num_Checkins'] + df.loc[i - 14, 'Num_Checkins']) / 2)
                    df.loc[i, 'Estimativa_Atendimentos'] = estimativa_dia
                    estimativas_semana.insert(i % 7, estimativa_dia)
                # Proximas semanas do mês
                else:
                    df.loc[i, 'Estimativa_Atendimentos'] = estimativas_semana[i % 7]

    return df


# Dataframe de Faturamentos - Base (orçado) e Zigpay (realizado)
def df_calculo_faturamento(df):

    # Ultimo dia com dados reais
    if idx_ultimo_dia_com_ticket_zig(df) < idx_ultimo_dia_com_faturamento_liquido(df):
        idx_ultimo_dia_zig = idx_ultimo_dia_com_ticket_zig(df)
    else:
        idx_ultimo_dia_zig = idx_ultimo_dia_com_faturamento_liquido(df)
    if idx_ultimo_dia_zig == None or idx_ultimo_dia_zig > df.index.max():
        return df
    ultimo_dia_zig = pd.to_datetime(df.loc[idx_ultimo_dia_zig, 'Data'])
    mes_ultimo_dia_zig = ultimo_dia_zig.month
    
    # Calcula o primeiro dia de estimativa
    idx_primeiro_dia_estimativa = idx_ultimo_dia_zig + 1
    if idx_primeiro_dia_estimativa > df.index.max():
        return df
    
    primeiro_dia = pd.to_datetime(df.loc[idx_primeiro_dia_estimativa, 'Data'])
    mes_primeiro_dia = primeiro_dia.month

    # Ultimo dia do mes
    ultimo_dia = get_last_day_of_month(primeiro_dia)
    num_estimativas = ultimo_dia - primeiro_dia.day
    idx_ultimo_dia_estimativa = idx_primeiro_dia_estimativa + num_estimativas

    if idx_ultimo_dia_zig != None and idx_primeiro_dia_estimativa in df.index and idx_ultimo_dia_estimativa in df.index:
        
        if mes_primeiro_dia != mes_ultimo_dia_zig:
            return df
        
        if not ('Estimativa_Faturamento' in df.columns):
            df['Estimativa_Faturamento'] = 0.0
        df['Faturamento_Base'] = df['Ticket_Base'] * df['Atendimentos_Base']
        df['Faturamento_Zigpay'] = df['Valor_Liquido']
        df['Estimativa_Faturamento'] = df['Estimativa_Ticket'] * df['Estimativa_Atendimentos']
        return df


def df_faturamento_por_dia(id_casa):

    # Obtém dataframe principal
    df = GET_DF_ITENS_VENDIDOS(id_casa)

    # Formata tipo de dados
    tipos_de_dados = {
        'Valor_Unit': float,
        'Qtde': int,
        'Desconto': float
    }
    df = df.astype(tipos_de_dados, errors='ignore')

    # Dataframe com valores brutos e liquidos
    df = df.assign(
        Valor_Bruto = lambda x: x['Valor_Unit'] * x['Qtde'],    
        Valor_Liquido = lambda x: x['Valor_Unit'] * x['Qtde'] - x['Desconto']
    )
    
    df_grouped = df.groupby('Data_Evento').agg({'Valor_Bruto': 'sum', 'Valor_Liquido': 'sum'}).reset_index()

    return df_grouped


def df_calculo_ticket_medio(df, coluna_faturamento, coluna_num_clientes):
    
    if not ('Ticket_Medio_Faturamento' in df.columns):
        df['Ticket_Medio_Faturamento'] = 0.0
    df['Ticket_Medio_Faturamento'] = df[coluna_faturamento] / df[coluna_num_clientes]

    return df
    
