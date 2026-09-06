from shutil import move

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from math import pi

# Obtém o diretório onde o arquivo tcc_teste.py está localizado
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_excel = os.path.join(diretorio_atual, 'dados_brutos_teste.xlsx')
# ============================================================
# 1. DADOS BRUTOS DO EXCEL
# ============================================================

try:
    df = pd.read_excel(caminho_excel, index_col=0)
except FileNotFoundError:
    print("Erro: o arquivo 'dados_brutos_teste.xlsx' não foi encontrado.")
    exit()

# ============================================================
# 2. NORMALIZAÇÃO LINEAR POR SOMA
# ============================================================

df_norm = df.copy().astype(float)

# Critérios de menor valor preferível
df_norm['Preço (R$)'] = 1 / df_norm['Preço (R$)']
df_norm['Qualidade (μm)'] = 1 / df_norm['Qualidade (μm)']

# Divisão pela soma da respectiva coluna
df_norm = df_norm / df_norm.sum()

# ============================================================
# 3. CÁLCULO DOS PESOS GAUSSIANOS
# ============================================================

medias = df_norm.mean()
desvios = df_norm.std(ddof=0)

fator_gauss = desvios / medias

pesos = fator_gauss / fator_gauss.sum()

# ============================================================
# 4. RANKING BASE
# ============================================================

ranking = df_norm.dot(pesos).sort_values(ascending=False)

# ============================================================
# 5. EXIBIÇÃO DO RESULTADO BASE
# ============================================================

print("\n--- MATRIZ NORMALIZADA ---")
print(df_norm.round(4))

print("\n--- TABELA DE PESOS GAUSSIANOS ---")

df_pesos = pd.DataFrame({
    'Média': medias,
    'Desvio Padrão': desvios,
    'Fator L (Gauss)': fator_gauss,
    'Peso Final (%)': pesos * 100
})

print(df_pesos.round(4))

print("\n--- RANKING BASE ---")
print(ranking.round(4))

# ============================================================
# 6. ANÁLISE DE SENSIBILIDADE DOS PESOS
# ============================================================

print("\n============================================================")
print("ANÁLISE DE SENSIBILIDADE - AUMENTO DE 10% DOS PESOS")
print("============================================================")

resultados_sensibilidade = {}
tabela_pesos_sensibilidade = {}

# Percorre cada critério individualmente
for criterio in pesos.index:

    # Copia os pesos originais
    novos_pesos = pesos.copy()

    # Aumenta somente o critério selecionado em 10%
    novos_pesos[criterio] = novos_pesos[criterio] * 1.10

    # Normaliza novamente para que a soma seja 1
    novos_pesos = novos_pesos / novos_pesos.sum()

    # Calcula novo ranking
    novo_ranking = df_norm.dot(novos_pesos).sort_values(ascending=False)

    # Guarda os resultados
    resultados_sensibilidade[criterio] = novo_ranking
    tabela_pesos_sensibilidade[criterio] = novos_pesos

    # Exibe no terminal
    print(f"\n--- Cenário: {criterio} +10% ---")

    print("\nNovos pesos:")
    print((novos_pesos * 100).round(4))

    print("\nNovo ranking:")
    print(novo_ranking.round(4))

# ============================================================
# 7. TABELA CONSOLIDADA DOS NOVOS PESOS
# ============================================================

df_sensibilidade_pesos = pd.DataFrame(
    tabela_pesos_sensibilidade
)

# Converter para porcentagem
df_sensibilidade_pesos = df_sensibilidade_pesos * 100

# Renomear colunas para facilitar leitura
df_sensibilidade_pesos.columns = [
    f'{criterio} +10%'
    for criterio in df_sensibilidade_pesos.columns
]

print("\n============================================================")
print("TABELA CONSOLIDADA - PESOS DA ANÁLISE DE SENSIBILIDADE")
print("============================================================")

print(df_sensibilidade_pesos.round(4))

# ============================================================
# 8. TABELA CONSOLIDADA DOS RANKINGS
# ============================================================

df_sensibilidade_ranking = pd.DataFrame(resultados_sensibilidade)

print("\n============================================================")
print("TABELA CONSOLIDADA - RANKINGS")
print("============================================================")

print(df_sensibilidade_ranking.round(4))

# ============================================================
# 9. EXPORTAÇÃO PARA EXCEL
# ============================================================

with pd.ExcelWriter('Teste_Sensibilidade_AHP_Gaussiano.xlsx') as writer:

    # Base
    df_norm.to_excel(
        writer,
        sheet_name='Matriz Normalizada'
    )

    df_pesos.to_excel(
        writer,
        sheet_name='Pesos Base'
    )

    ranking.to_excel(
        writer,
        sheet_name='Ranking Base'
    )

    # Sensibilidade
    df_sensibilidade_pesos.to_excel(
        writer,
        sheet_name='Sensibilidade Pesos'
    )

    df_sensibilidade_ranking.to_excel(
        writer,
        sheet_name='Sensibilidade Ranking'
    )
move("C:\\Users\\netoc\\AppData\\Local\\Programs\\Microsoft VS Code\\Teste_Sensibilidade_AHP_Gaussiano.xlsx", "C:\\Users\\netoc\\Documents\\TCC - TESTE SENSIBILIDADE\\")
print("\nArquivo 'Teste_Sensibilidade_AHP_Gaussiano.xlsx' criado com sucesso.")   