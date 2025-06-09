
from preprocessamento import carregar_e_limpar_dados
from grafo_areas import gerar_pares_areas_similares_por_ano, construir_grafos_por_ano

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import csv
import random
import os
from community import modularity

# === Etapa 1: carregamento do dataset ===
caminho_dataset = os.path.join(os.path.dirname(__file__), "datasetReal.csv") #MUDAR ESTILO DE PLOTAGEM CASO ALTERAR O DATASET
df = carregar_e_limpar_dados(caminho_dataset)

print("\nConstruindo grafos de áreas LAPD por ano...")
conexoes_por_ano = gerar_pares_areas_similares_por_ano(df)
grafos_por_ano = construir_grafos_por_ano(conexoes_por_ano)

# Visualizar e exportar grafos de áreas por ano
for ano, grafo_areas in grafos_por_ano.items():
    print(f"✔ Exportando e salvando visualização para o ano {ano}...")

    # Salvar imagem do grafo
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

    # Exportar grafo para Gephi
    try:
        nx.write_gexf(grafo_areas, f"grafo_areas_{ano}.gexf")
    except Exception as e:
        print(f"❌ Erro ao exportar grafo de {ano}: {e}")

# === Etapa 5: Métricas ===
print("\nCalculando métricas de centralidade e modularidade...")