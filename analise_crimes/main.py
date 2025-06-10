import igraph as ig
import leidenalg
import matplotlib.pyplot as plt
import networkx as nx
import os
import matplotlib
matplotlib.use('TkAgg')

from preprocessamento import carregar_e_limpar_dados
from grafo_areas import gerar_pares_areas_similares_por_ano, construir_grafos_por_ano, construir_grafo_total


def aplicar_leiden_e_analisar(grafo_nx, nome_grafo, contagem_por_area):
    print(f"\n🔍 Processando comunidades do {nome_grafo}...")

    grafo_ig = ig.Graph()
    grafo_ig.add_vertices(list(grafo_nx.nodes))
    grafo_ig.add_edges(list(grafo_nx.edges))

    pesos = [grafo_nx[u][v].get('weight', 1.0) for u, v in grafo_nx.edges]
    grafo_ig.es['weight'] = pesos

    particao = leidenalg.find_partition(grafo_ig, leidenalg.ModularityVertexPartition, weights='weight', seed=42)

    modularidade = particao.modularity
    print(f"   ➞ Modularidade: {modularidade:.4f}")
    print(f"   ➞ Número de comunidades: {len(particao)}")

    comunidades = {grafo_ig.vs[i]['name']: cid for i, cid in enumerate(particao.membership)}

    pesos_comunidade = {}
    registros_comunidade = {}

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
        print(f"\n      ➞ Comunidade {cid}: peso total interno = {peso_total}, registros = {total_registros}, proporção = {proporcao:.4f}")

        print("         Áreas e seus graus ponderados:")

        areas_comunidade = [area for area, com_id in comunidades.items() if com_id == cid]

        for area in sorted(areas_comunidade):
            grau_ponderado = grafo_nx.degree(area, weight='weight') if grafo_nx.has_node(area) else 0
            registros_area = contagem_por_area.get(area, 0)
            print(f"            - {area}: registros = {registros_area}, grau ponderado = {grau_ponderado}")


# ============== Etapa 1: carregamento do dataset ==============
caminho_dataset = os.path.join(os.path.dirname(__file__), "datasetReal.csv")
df = carregar_e_limpar_dados(caminho_dataset)


# ============== Etapa 2: Grafos por ano ==============
print("\nConstruindo grafos de áreas LAPD por ano...")
conexoes_por_ano, contagem_por_area = gerar_pares_areas_similares_por_ano(df)
grafos_por_ano = construir_grafos_por_ano(conexoes_por_ano)

for ano, grafo_areas in grafos_por_ano.items():
    print(f"\n✔ Exportando visualização para o ano {ano}...")

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(grafo_areas, seed=42)
    nx.draw(grafo_areas, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=8)
    nx.draw_networkx_edge_labels(
        grafo_areas, pos,
        edge_labels={(u, v): d['weight'] for u, v, d in grafo_areas.edges(data=True)},
        font_size=6
    )
    plt.title(f"Grafo de Áreas - LAPD ({ano})")
    plt.savefig(f"grafo_areas_{ano}.png", dpi=300)
    plt.close()

    # Aplicar Leiden e analisar
    aplicar_leiden_e_analisar(grafo_areas, f"ano {ano}", contagem_por_area)


# ============== Etapa 3: Grafo Total ==============
grafo_total = construir_grafo_total(df)
print("\n✔ Exportando visualização do grafo total...")

plt.figure(figsize=(10, 8))
pos = nx.spring_layout(grafo_total, seed=42)
nx.draw(grafo_total, pos, with_labels=True, node_color='lightgreen', node_size=800, font_size=8)
nx.draw_networkx_edge_labels(
    grafo_total, pos,
    edge_labels={(u, v): d['weight'] for u, v, d in grafo_total.edges(data=True)},
    font_size=6
)
plt.title("Grafo Total de Áreas - LAPD")
plt.savefig("grafo_areas_total.png", dpi=300)
plt.close()

# Aplicar Leiden e analisar no grafo total
aplicar_leiden_e_analisar(grafo_total, "grafo total", contagem_por_area)