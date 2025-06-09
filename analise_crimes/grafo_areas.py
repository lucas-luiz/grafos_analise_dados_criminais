import networkx as nx
from collections import defaultdict
from itertools import combinations
from tqdm import tqdm

def construir_grafo_geografico(conexoes):
    G = nx.Graph()
    areas = set([a for pair in conexoes for a in pair])
    G.add_nodes_from(areas)

    for (a1, a2), peso in conexoes.items():
        G.add_edge(a1, a2, weight=peso)

    return G

# === Funções novas para grafos por ano ===

def gerar_pares_areas_similares_por_ano(df):
    df["ANO"] = df["Date Rptd"].dt.year
    conexoes_por_ano = {}

    for ano, df_ano in df.groupby("ANO"):
        grupos = df_ano.groupby(["Mocodes", "Crm Cd Desc", df["Date Rptd"].dt.date])
        conexoes = defaultdict(int)

        for _, grupo in grupos:
            areas = grupo["AREA NAME"]
            for a1, a2 in combinations(sorted(areas), 2):
                conexoes[(a1, a2)] += 1

        conexoes_por_ano[ano] = conexoes

    return conexoes_por_ano

def construir_grafos_por_ano(conexoes_por_ano):
    grafos = {}
    for ano, conexoes in conexoes_por_ano.items():
        grafos[ano] = construir_grafo_geografico(conexoes)
    return grafos
