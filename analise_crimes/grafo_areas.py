import networkx as nx
from collections import defaultdict
from itertools import combinations
from tqdm import tqdm

def gerar_pares_areas_similares(df):
    grupos = df.groupby(["Mocodes", "Crm Cd Desc", df["DATE OCC"].dt.date])
    conexoes = defaultdict(int)

    for _, grupo in tqdm(grupos):
        areas = grupo["AREA NAME"].unique()
        for a1, a2 in combinations(sorted(areas), 2):
            conexoes[(a1, a2)] += 1

    return conexoes

def construir_grafo_geografico(conexoes):
    G = nx.Graph()
    areas = set([a for pair in conexoes for a in pair])
    G.add_nodes_from(areas)

    for (a1, a2), peso in conexoes.items():
        G.add_edge(a1, a2, weight=peso)

    return G
