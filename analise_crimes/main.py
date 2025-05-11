from preprocessamento import carregar_e_limpar_dados
from grafo_crimes import construir_grafo_de_crimes, aplicar_louvain
from grafo_areas import gerar_pares_areas_similares, construir_grafo_geografico

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import csv
from community import modularity

# === Etapa 1: carregamento do dataset ===
df = carregar_e_limpar_dados(
    r"C:\Users\jv_ar\OneDrive\Área de Trabalho\Grafos do Inferno\Travalho repositório\grafos_analise_dados_criminais\analise_crimes\dataset.csv"
)
df = df.head(1000)  # amostra reduzida

# === Etapa 2: GRAFO DE CRIMES SIMILARES ===
print("\nConstruindo grafo de crimes...")
grafo_crimes = construir_grafo_de_crimes(df)
particoes = aplicar_louvain(grafo_crimes)
nx.set_node_attributes(grafo_crimes, particoes, "comunidade")

# Visualização
cores = [particoes[n] for n in grafo_crimes.nodes()]
plt.figure("Comunidades de Crimes (grafo de similaridade)")
nx.draw_spring(grafo_crimes, node_color=cores, node_size=20, with_labels=False)
plt.title("Comunidades de crimes (grafo de similaridade)")
plt.savefig("grafo_crimes.png", dpi=300)

# === Etapa 3: GRAFO GEOGRÁFICO ENTRE ÁREAS ===
print("\nConstruindo grafo de áreas LAPD...")
conexoes = gerar_pares_areas_similares(df)
grafo_areas = construir_grafo_geografico(conexoes)

plt.figure("Conexões entre Áreas LAPD")
pos = nx.spring_layout(grafo_areas, seed=42)
nx.draw(grafo_areas, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=8)
nx.draw_networkx_edge_labels(
    grafo_areas, pos,
    edge_labels={(u, v): d['weight'] for u, v, d in grafo_areas.edges(data=True)},
    font_size=6
)
plt.title("Conexões entre Áreas (grafo geográfico)")
plt.savefig("grafo_areas.png", dpi=300)

# Mostrar os gráficos
plt.show()

# === Etapa 4: Exportar grafos para Gephi ===
print("\nExportando grafos para Gephi (.gexf)...")

# Corrigir atributos inválidos
for node, attrs in grafo_crimes.nodes(data=True):
    for key in list(attrs.keys()):
        if isinstance(attrs[key], (pd.Timestamp, type)):
            del grafo_crimes.nodes[node][key]

try:
    nx.write_gexf(grafo_crimes, "grafo_crimes.gexf")
    print("✔ grafo_crimes.gexf exportado com sucesso.")
except Exception as e:
    print("❌ Erro ao exportar grafo_crimes.gexf:", e)

try:
    nx.write_gexf(grafo_areas, "grafo_areas.gexf")
    print("✔ grafo_areas.gexf exportado com sucesso.")
except Exception as e:
    print("❌ Erro ao exportar grafo_areas.gexf:", e)

try:
    nx.write_graphml(grafo_crimes, "grafo_crimes.graphml")
    print("✔ grafo_crimes.graphml exportado como alternativa.")
except Exception as e:
    print("❌ Erro ao exportar grafo_crimes.graphml:", e)

# === Etapa 5: Métricas ===
print("\nCalculando métricas de centralidade e modularidade...")

grau_dict = dict(grafo_crimes.degree())
nx.set_node_attributes(grafo_crimes, grau_dict, "grau")

betweenness = nx.betweenness_centrality(grafo_crimes)
nx.set_node_attributes(grafo_crimes, betweenness, "betweenness")

mod = modularity(particoes, grafo_crimes)
print(f"✔ Modularidade (Louvain): {mod:.4f}")

top_grau = sorted(grau_dict.items(), key=lambda x: x[1], reverse=True)[:5]
print("\nTop 5 crimes com maior grau:")
for idx, valor in top_grau:
    print(f"  ID {idx} — Grau: {valor}, Tipo: {grafo_crimes.nodes[idx]['Crm Cd Desc']}")

top_bet = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]
print("\nTop 5 crimes com maior centralidade de intermediação:")
for idx, valor in top_bet:
    print(f"  ID {idx} — Betweenness: {valor:.5f}, Tipo: {grafo_crimes.nodes[idx]['Crm Cd Desc']}")

# Exportar para CSV
with open("metricas_crimes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Grau", "Betweenness", "Comunidade", "Tipo de Crime"])
    for n in grafo_crimes.nodes():
        writer.writerow([
            n,
            grafo_crimes.nodes[n].get("grau", ""),
            grafo_crimes.nodes[n].get("betweenness", ""),
            grafo_crimes.nodes[n].get("comunidade", ""),
            grafo_crimes.nodes[n].get("Crm Cd Desc", "")
        ])
print("✔ Métricas exportadas para metricas_crimes.csv")
