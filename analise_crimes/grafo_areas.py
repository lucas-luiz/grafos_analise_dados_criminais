import networkx as nx
import leidenalg
import igraph as ig
from collections import defaultdict
from itertools import combinations
import numpy as np


# ============================== Construir Grafo ==============================
def construir_grafo(conexoes):
    G = nx.Graph()
    areas = set([a for pair in conexoes for a in pair])
    G.add_nodes_from(areas)

    for (a1, a2), peso in conexoes.items():
        G.add_edge(a1, a2, weight=peso)

    return G


# ============================== Tratar Grafo Por Ano ==============================
def construir_grafos_por_ano(conexoes_por_ano):
    grafos = {}
    for ano, conexoes in conexoes_por_ano.items():
        grafos[ano] = construir_grafo(conexoes)
    return grafos

def gerar_pares_por_ano(df):
    df["ANO"] = df["Date Rptd"].dt.year
    conexoes_por_ano = {}
    contagem_por_ano = {}
    contagem_por_ano["total"] = defaultdict(int)

    for ano, df_ano in df.groupby("ANO"):
        grupos = df_ano.groupby(["Mocodes", "Crm Cd Desc"])
        conexoes = defaultdict(int)
        contagem_por_ano[ano] = defaultdict(int)

        for _, grupo in grupos:
            areas = grupo["AREA NAME"]
            for area in areas:
                contagem_por_ano[ano][area] += 1
                contagem_por_ano["total"][area] += 1
            for a1, a2 in combinations(sorted(areas), 2):
                conexoes[(a1, a2)] += 1

        conexoes_por_ano[ano] = conexoes

    return construir_grafos_por_ano(conexoes_por_ano), contagem_por_ano


# ============================== Tratar Grafo Total ==============================
def gerar_pares_total(df):
    grupos = df.groupby(["Mocodes", "Crm Cd Desc", df["Date Rptd"].dt.date])
    conexoes_total = defaultdict(int)

    for _, grupo in grupos:
        areas = grupo["AREA NAME"]
        for a1, a2 in combinations(sorted(areas), 2):
            conexoes_total[(a1, a2)] += 1

    return construir_grafo(conexoes_total)


# ============================== Leiden ==============================
def aplicar_leiden_e_analisar(grafo_nx, contagem_por_area):
    grafo_ig = ig.Graph()
    grafo_ig.add_vertices(list(grafo_nx.nodes))
    grafo_ig.add_edges(list(grafo_nx.edges))

    pesos = [grafo_nx[u][v].get('weight', 1.0) for u, v in grafo_nx.edges]
    grafo_ig.es['weight'] = pesos

    particao = leidenalg.find_partition(
        grafo_ig,
        leidenalg.RBConfigurationVertexPartition,
        resolution_parameter=1, #Ajustavel, quanto maior mais comunidades
        weights='weight',
        seed=42
    )
    comunidades = {grafo_ig.vs[i]['name']: cid for i, cid in enumerate(particao.membership)}

    pesos_comunidade = {}
    registros_comunidade = {}
    dados_comunidades = {}

    for area, cid in comunidades.items():
        registros_comunidade[cid] = registros_comunidade.get(cid, 0) + contagem_por_area.get(area, 0)

    for eid in range(len(grafo_ig.es)):
        v1 = grafo_ig.vs[grafo_ig.es[eid].source]['name']
        v2 = grafo_ig.vs[grafo_ig.es[eid].target]['name']
        w = grafo_ig.es[eid]['weight']
        c1 = comunidades[v1]
        c2 = comunidades[v2]
        if c1 == c2:
            pesos_comunidade[c1] = pesos_comunidade.get(c1, 0) + w

    for cid in pesos_comunidade:
        peso_total = pesos_comunidade[cid]
        total_registros = registros_comunidade.get(cid, 1)
        proporcao = peso_total / total_registros if total_registros > 0 else 0

        areas_comunidade = sorted(set(area for area, com_id in comunidades.items() if com_id == cid))
        dados_area = {}

        for area in sorted(areas_comunidade):
            grau_ponderado = grafo_nx.degree(area, weight='weight') if grafo_nx.has_node(area) else 0
            registros_area = contagem_por_area.get(area, 0)
            dados_area[area] = {"registros_area": registros_area,
                                "grau_ponderado": grau_ponderado}
        
        dados_comunidades[cid] = {'peso_total': peso_total,
                                  "total_registros": total_registros,
                                  "proporcao": proporcao,
                                  "dados_area": dados_area}

    return particao, dados_comunidades


def layout_por_comunidade(grafo, particao, escala_comunidade=5, escala_local=1):
    comunidades = {}
    for node, cid in zip(grafo.nodes, particao.membership):
        comunidades.setdefault(cid, []).append(node)

    # Layout das comunidades (meta-grafo)
    meta_grafo = nx.Graph()
    for cid in comunidades:
        meta_grafo.add_node(cid)
    for u, v in grafo.edges:
        cu = particao.membership[list(grafo.nodes).index(u)]
        cv = particao.membership[list(grafo.nodes).index(v)]
        if cu != cv:
            meta_grafo.add_edge(cu, cv)

    pos_comunidades = nx.spring_layout(meta_grafo, scale=escala_comunidade, seed=42)

    # Layout dentro de cada comunidade
    pos_final = {}
    for cid, nodes in comunidades.items():
        subgrafo = grafo.subgraph(nodes)
        centro = pos_comunidades[cid]
        pos_local = nx.spring_layout(subgrafo, scale=escala_local, seed=42)
        for n in subgrafo.nodes:
            offset = np.array(pos_local[n])
            pos_final[n] = centro + offset  # posição global

    return pos_final
