
import networkx as nx
from tqdm import tqdm
import igraph as ig
import leidenalg
import matplotlib.pyplot as plt
import numpy as np

def calcular_peso_similaridade(c1, c2):
    """
    Cálculo do peso da aresta entre dois crimes.
    Fórmula formal:
    w(i,j) = 2 * I(CrmCdDesc_i == CrmCdDesc_j) +
             1 * I(AREA_i == AREA_j) +
             1 * I(|DATE_i - DATE_j| <= 3 dias) +
             2 * I(Mocodes_i == Mocodes_j)
    """
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

def networkx_to_igraph(G_nx):
    G_ig = ig.Graph()
    nodes = list(G_nx.nodes())
    G_ig.add_vertices(nodes)

    edges = [(u, v) for u, v in G_nx.edges()]
    G_ig.add_edges(edges)

    weights = [G_nx[u][v].get('weight', 1.0) for u, v in G_nx.edges()]
    G_ig.es['weight'] = weights

    # name attribute for consistency
    for idx, node in enumerate(nodes):
        G_ig.vs[idx]['name'] = node

    return G_ig

def aplicar_leiden(G_nx):
    G_ig = networkx_to_igraph(G_nx)
    partition = leidenalg.find_partition(G_ig, leidenalg.ModularityVertexPartition, weights='weight')

    particoes = {}
    for comunidade_id, membros in enumerate(partition):
        for node_id in membros:
            node_name = G_ig.vs[node_id]['name']
            particoes[node_name] = comunidade_id

    return particoes

def verificar_scale_free(G_nx, save_fig=False, fig_name="distribuicao_grau.png"):
    """
    Verifica se a rede segue um padrão de rede livre de escala (scale-free).
    Plota a distribuição de grau em escala log-log.
    """
    grau_sequence = sorted([d for n, d in G_nx.degree()], reverse=True)
    grau_counts = np.bincount(grau_sequence)
    grau_vals = np.arange(len(grau_counts))

    # Evitar zeros
    nonzero_idx = grau_counts > 0

    plt.figure(figsize=(6, 4))
    plt.loglog(grau_vals[nonzero_idx], grau_counts[nonzero_idx], marker='o', linestyle='none')
    plt.xlabel("Grau (k)")
    plt.ylabel("P(k)")
    plt.title("Distribuição de Grau - Verificação Scale-Free")
    plt.grid(True, which="both", ls="--")

    if save_fig:
        plt.savefig(fig_name, dpi=300)

    plt.close()
