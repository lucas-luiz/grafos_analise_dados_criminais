import matplotlib.pyplot as plt
import networkx as nx
import os

from preprocessamento import carregar_e_limpar_dados
from grafo_areas import gerar_pares_por_ano, gerar_pares_total, aplicar_leiden_e_analisar


# ============================== Etapa 1: carregamento do dataset ==============================
caminho_dataset = os.path.join(os.path.dirname(__file__), "datasetReal.csv")
df = carregar_e_limpar_dados(caminho_dataset)


# ============================== Etapa 2: Grafos por ano ==============================
print("\nConstruindo grafos de áreas LAPD por ano...")
grafos_por_ano, contagem_por_ano = gerar_pares_por_ano(df)

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
    print(f"\n🔍 Processando comunidades do ano {ano}...")
    particao, dados_comunidades = aplicar_leiden_e_analisar(grafo_areas, contagem_por_ano[ano])
    
    print(f"   ➞ Modularidade: {particao.modularity:.4f}")
    print(f"   ➞ Número de comunidades: {len(particao)}")

    for cid, comunidade in dados_comunidades.items():
        print(f"\n      ➞ Comunidade {cid}: peso total interno = {comunidade['peso_total']}, registros = {comunidade['total_registros']}, proporção = {comunidade['proporcao']:.4f}") 
        print("         Áreas e seus graus ponderados:")

        for area_name, areas in comunidade["dados_area"].items():
            print(f"            - {area_name}: registros = {areas['registros_area']}, grau ponderado = {areas['grau_ponderado']}")


# ============================== Etapa 3: Grafo Total ==============================
grafo_total = gerar_pares_total(df)
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
print(f"\n🔍 Processando comunidades do grafo total...")
particao, dados_comunidades = aplicar_leiden_e_analisar(grafo_total, contagem_por_ano["total"])

print(f"   ➞ Modularidade: {particao.modularity:.4f}")
print(f"   ➞ Número de comunidades: {len(particao)}")

for cid, comunidade in dados_comunidades.items():
    print(f"\n      ➞ Comunidade {cid}: peso total interno = {comunidade['peso_total']}, registros = {comunidade['total_registros']}, proporção = {comunidade['proporcao']:.4f}") 
    print("         Áreas e seus graus ponderados:")

    for area_name, areas in comunidade["dados_area"].items():
        print(f"            - {area_name}: registros = {areas['registros_area']}, grau ponderado = {areas['grau_ponderado']}")