import streamlit as st
import pandas as pd
import datetime
from utils.functions.date_functions import *

# Dataframe de Faturamentos - Base (orçado) e Zigpay (realizado)
def df_calculo_faturamento(df):
    df['Faturamento_Base'] = df['Ticket_Base'] * df['Atendimentos_Base']
    df['Faturamento_Zigpay'] = df['Ticket_Zig'] * df['Atendimentos_Zig']
    return df[['Casa', 'Data', 'Faturamento_Base', 'Faturamento_Zigpay']]


# Obter lista de datas de num_semanas anteriores para a data fornecida
def list_ultimos_dias_da_semana(data, num_semanas):
    """
    @param data: Data da qual se quer obter os dias das semanas anteriores
    @param num_semanas: Número de semanas anteriores
    @return: Lista com as datas dos dias de num_semanas anteriores
    """
    lista_dias_semanas_anteriores = []
    # Adiciona o dia atual à lista
    lista_dias_semanas_anteriores.append(data)
    # Adiciona os dias das semanas anteriores à lista
    for i in range(num_semanas):
        data -= pd.DateOffset(days=7)
        lista_dias_semanas_anteriores.append(data)
    return lista_dias_semanas_anteriores


# Dataframe filtrado pela casa:
def df_filtrar_casa(df, id_casa):
    df_filtrado = df[df['Casa'] == id_casa]
    return df_filtrado


def idx_ultimo_dia_com_ticket_zig(df):
    indices_ticket_zig = df.loc[df['Ticket_Zig'] != 0].index

    if len(indices_ticket_zig) == 0:
        return None
    return max(indices_ticket_zig)


# Estimativa de Ticket para o primeiro mes
def df_estimativa_ticket_proximo_mes(df):

    # Ultimo dia com dados reais
    idx_ultimo_dia_zig = idx_ultimo_dia_com_ticket_zig(df)
    if idx_ultimo_dia_zig == None or idx_ultimo_dia_zig > df.index.max():
        return df
    ultimo_dia_zig = datetime.datetime.strptime(df.loc[idx_ultimo_dia_zig, 'Data'], "%d-%m-%Y")
    mes_ultimo_dia_zig = ultimo_dia_zig.month
    
    # Calcula o primeiro dia de estimativa
    idx_primeiro_dia_estimativa = idx_ultimo_dia_zig + 1
    if idx_primeiro_dia_estimativa > df.index.max():
        return df
    
    primeiro_dia = datetime.datetime.strptime(df.loc[idx_primeiro_dia_estimativa, 'Data'], '%d-%m-%Y')
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
                    estimativa_dia = (df.loc[i - 7, 'Ticket_Zig'] + df.loc[i - 14, 'Ticket_Zig']) / 2
                    df.loc[i, 'Estimativa_Ticket'] = estimativa_dia
                    estimativas_semana.insert(i % 7, estimativa_dia)
                # Proximas semanas do mês
                else:
                    df.loc[i, 'Estimativa_Ticket'] = estimativas_semana[i % 7]


            df = df[['Casa', 'Data', 'Ticket_Base', 'Ticket_Zig', 'Estimativa_Ticket']]

    return df


# Dataframe das estimativas - Atendimentos (até 1 mês)
def df_estimativa_atendimentos(df):
    idx_ultimo_dia_zig = idx_ultimo_dia_com_ticket_zig(df)
    
    if idx_ultimo_dia_zig != None:
        idx_primeiro_dia_estimativa = idx_ultimo_dia_zig + 1
        idx_ultimo_dia_estimativa = idx_primeiro_dia_estimativa + 30
        
        # Verifica se o dataframe já possui a coluna 'Estimativa_Ticket'
        # Se não existir, cria a coluna com valor 0.0 como padrão
        if not ('Estimativa_Atendimentos' in df.columns):
            df['Estimativa_Atendimentos'] = 0.0

        for i in df.index[idx_primeiro_dia_estimativa:idx_ultimo_dia_estimativa + 1]:
            # Verifica se o dia já existe no dataframe
            if i in df.index[idx_primeiro_dia_estimativa:idx_primeiro_dia_estimativa + 7]:
                # Se o dia está no intervalo, atualiza a estimativa com o ticket médio do dia 7 dias antes e de 14 dias antes
                df.loc[i, 'Estimativa_Atendimentos'] = (df.loc[i - 7, 'Atendimentos_Zig'] + df.loc[i - 14, 'Atendimentos_Zig']) / 2

        df = df[['Casa', 'Data', 'Atendimentos_Base', 'Atendimentos_Zig', 'Estimativa_Atendimentos']]

    return df









# def df_estimativa_ticket(df):
    
#     colunas_necessarias = ['Atendimentos_Zigpay', 'Ticket_Zigpay']
#     if not all(coluna in df.columns for coluna in colunas_necessarias):
#         st.error("As colunas necessárias não estão presentes no DataFrame.")
#     df['Estimativa_Ticket'] = 
