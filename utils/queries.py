

GET_CASAS = """
WITH empresas_normalizadas AS (
  SELECT
    CASE 
      WHEN ID IN (161, 162) THEN 149
      ELSE ID
    END AS ID_Casa_Normalizada,
    NOME_FANTASIA,
    FK_GRUPO_EMPRESA
  FROM T_EMPRESAS
)
SELECT
  te.ID_Casa_Normalizada AS ID_Casa,
  te2.NOME_FANTASIA AS Casa
FROM empresas_normalizadas te
LEFT JOIN T_EMPRESAS te2 ON te.ID_Casa_Normalizada = te2.ID
WHERE te.FK_GRUPO_EMPRESA = 100
GROUP BY te.ID_Casa_Normalizada, te2.NOME_FANTASIA
ORDER BY te2.NOME_FANTASIA
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
