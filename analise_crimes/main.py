import matplotlib.pyplot as plt
import networkx as nx
import os

from preprocessamento import carregar_e_limpar_dados
from grafo_areas import gerar_pares_por_ano, gerar_pares_total, aplicar_leiden_e_analisar, layout_por_comunidade

# ============================== Carregamento dos Dados ==============================
caminho_dataset = os.path.join(os.path.dirname(__file__), "datasetReal.csv")
df = carregar_e_limpar_dados(caminho_dataset)

# ============================== Análise por Ano ==============================
print("\nConstruindo grafos de áreas LAPD por ano...")
grafos_por_ano, contagem_por_ano = gerar_pares_por_ano(df)

for ano, grafo_areas in grafos_por_ano.items():
    # Exibe grau ponderado (número de conexões ponderadas) de cada área no ano
    print(f"\nGrau ponderado dos nós no grafo do ano {ano}:")
    for no in grafo_areas.nodes():
        grau_ponderado = grafo_areas.degree(no, weight='weight')
        print(f"    {no}: {grau_ponderado}")

    # Exporta visualização antes do Leiden
    plt.figure(figsize=(8, 6))
    pos_padrao = nx.spring_layout(grafo_areas, seed=42)
    nx.draw(grafo_areas, pos_padrao, with_labels=True, node_color='lightblue', node_size=800, font_size=8)
    nx.draw_networkx_edge_labels(
        grafo_areas, pos_padrao,
        edge_labels={(u, v): d['weight'] for u, v, d in grafo_areas.edges(data=True)},
        font_size=6
    )
    plt.title(f"Grafo de Áreas - LAPD ({ano}) - Antes do Leiden")
    plt.savefig(f"grafo_areas_{ano}_antes.png", dpi=300)
    plt.close()

    # Aplica Leiden
    print(f"\n Processando comunidades do ano {ano}...")
    particao, dados_comunidades = aplicar_leiden_e_analisar(grafo_areas, contagem_por_ano[ano])
    print(f"    Modularidade: {particao.modularity:.4f}")
    print(f"    Número de comunidades: {len(particao)}")

    # Exibe estatísticas por comunidade
    for cid, comunidade in dados_comunidades.items():
        print(f"\n       Comunidade {cid}: peso total interno = {comunidade['peso_total']}, registros = {comunidade['total_registros']}, proporção = {comunidade['proporcao']:.4f}")
        for area_name, areas in comunidade["dados_area"].items():
            print(f"            - {area_name}: registros = {areas['registros_area']}, grau ponderado = {areas['grau_ponderado']}")

    # Exporta visualização pós-Leiden
    comunidades = {name: cid for name, cid in zip(grafo_areas.nodes, particao.membership)}
    cores = [comunidades[node] for node in grafo_areas.nodes]
    pos_comunidades = layout_por_comunidade(grafo_areas, particao)
    plt.figure(figsize=(8, 6))
    nx.draw(
        grafo_areas, pos_comunidades,
        with_labels=True,
        node_color=cores,
        cmap=plt.cm.tab20,
        node_size=800,
        font_size=8
    )
    nx.draw_networkx_edge_labels(
        grafo_areas, pos_comunidades,
        edge_labels={(u, v): d['weight'] for u, v, d in grafo_areas.edges(data=True)},
        font_size=6
    )
    plt.title(f"Grafo de Áreas - LAPD ({ano}) - Com Comunidades (Leiden)")
    plt.savefig(f"grafo_areas_{ano}_depois.png", dpi=300)
    plt.close()

# ============================== Análise do Grafo Total ==============================
print("\nConstruindo grafo total...")
grafo_total = gerar_pares_total(df)

# Exibe grau ponderado dos nós no grafo total
print("\nGrau ponderado dos nós no grafo TOTAL:")
for no in grafo_total.nodes():
    grau_ponderado = grafo_total.degree(no, weight='weight')
    print(f"    {no}: {grau_ponderado}")

# Exporta visualização antes do Leiden
plt.figure(figsize=(10, 8))
pos_total = nx.spring_layout(grafo_total, seed=42)
nx.draw(grafo_total, pos_total, with_labels=True, node_color='lightblue', node_size=800, font_size=8)
nx.draw_networkx_edge_labels(
    grafo_total, pos_total,
    edge_labels={(u, v): d['weight'] for u, v, d in grafo_total.edges(data=True)},
    font_size=6
)
plt.title("Grafo Total de Áreas - Antes do Leiden")
plt.savefig("grafo_areas_total_antes.png", dpi=300)
plt.close()

# Aplica Leiden ao grafo total
print(f"\n Processando comunidades do grafo total...")
particao_total, dados_comunidades = aplicar_leiden_e_analisar(grafo_total, contagem_por_ano["total"])
print(f"    Modularidade: {particao_total.modularity:.4f}")
print(f"    Número de comunidades: {len(particao_total)}")

# Exibe estatísticas por comunidade
for cid, comunidade in dados_comunidades.items():
    print(f"\n       Comunidade {cid}: peso total interno = {comunidade['peso_total']}, registros = {comunidade['total_registros']}, proporção = {comunidade['proporcao']:.4f}")
    for area_name, areas in comunidade["dados_area"].items():
        print(f"            - {area_name}: registros = {areas['registros_area']}, grau ponderado = {areas['grau_ponderado']}")

# Exporta visualização pós-Leiden
comunidades_total = {name: cid for name, cid in zip(grafo_total.nodes, particao_total.membership)}
cores_total = [comunidades_total[node] for node in grafo_total.nodes]
pos_comunidades_total = layout_por_comunidade(grafo_total, particao_total)

plt.figure(figsize=(10, 8))
nx.draw(
    grafo_total, pos_comunidades_total,
    with_labels=True,
    node_color=cores_total,
    cmap=plt.cm.tab20,
    node_size=800,
    font_size=8
)
nx.draw_networkx_edge_labels(
    grafo_total, pos_comunidades_total,
    edge_labels={(u, v): d['weight'] for u, v, d in grafo_total.edges(data=True)},
    font_size=6
)
plt.title("Grafo Total de Áreas - Com Comunidades (Leiden)")
plt.savefig("grafo_areas_total_depois.png", dpi=300)
plt.close()