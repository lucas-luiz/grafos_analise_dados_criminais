import networkx as nx
from community import community_louvain
from tqdm import tqdm

def calcular_peso_similaridade(c1, c2):
    peso = 0
    if c1["Crm Cd Desc"] == c2["Crm Cd Desc"]:
        peso += 2
    if c1["AREA NAME"] == c2["AREA NAME"]:
        peso += 1
    if abs((c1["DATE OCC"] - c2["DATE OCC"]).days) <= 3:
        peso += 1
    if c1["Mocodes"] == c2["Mocodes"]:
        peso += 2
    return peso

def construir_grafo_de_crimes(df, peso_min=3):
    G = nx.Graph()

    for idx, row in df.iterrows():
        G.add_node(idx, **row)

    for i in tqdm(range(len(df))):
        for j in range(i+1, len(df)):
            peso = calcular_peso_similaridade(df.loc[i], df.loc[j])
            if peso >= peso_min:
                G.add_edge(i, j, weight=peso)

    return G

def aplicar_louvain(G):
    return community_louvain.best_partition(G, weight='weight')
