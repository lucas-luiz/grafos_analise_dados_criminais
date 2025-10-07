# 🕸️ Análise de Dados Criminais em Grafos

Projeto desenvolvido para a disciplina **Algoritmos em Grafos** — UNIFEI (2024).  
O objetivo foi aplicar conceitos de **Teoria dos Grafos** e **Análise de Redes Complexas** em dados reais de criminalidade da cidade de **Los Angeles (2020–2024)**.

---

## 🎯 Objetivo

Modelar relações entre diferentes regiões da cidade como um grafo, onde:
- **Nós** representam regiões geográficas;
- **Arestas** representam relações entre crimes ocorridos em regiões próximas ou com características semelhantes.

O projeto busca identificar padrões de conectividade, comunidades criminais e regiões com papel central (hubs) na rede.

---

## ⚙️ Tecnologias e Ferramentas

- **Python 3**
- **NetworkX** — modelagem e análise de grafos  
- **Pandas / NumPy** — manipulação e limpeza de dados  
- **Matplotlib / Plotly** — visualização  
- **Algoritmo de Leiden** — detecção de comunidades  
- **Jupyter Notebook / VS Code**

---

## 📊 Resultados

- Identificação de **estruturas livres de escala** (hubs de criminalidade);
- **Comunidades regionais** bem definidas usando o algoritmo de Leiden;
- Análise temporal de **evolução de crimes (2020–2024)**;
- Visualizações interativas dos grafos e mapas de calor.

---

## 🔧 Como executar

1. **Baixe o dataset:**  
   [Google Drive - Dataset LAPD](https://drive.google.com/file/d/1V4WXbPOqK4rUxwKEqMy3oOje-5F7e150/view?usp=sharing)

2. **Coloque o arquivo na pasta:**

    analise_crimes/

    E renomeie para: "datasetReal"

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Execute o script principal:**
```bash
python analise_crimes/main.py
```

---

## 👥 Autores

- Lucas Luiz da Silva
- Luiz Augusto Silva
- Paulo Alexandre de Oliveira Nascimento Filho

Trabalho orientado pelo Prof. Rafael Frinhani — UNIFEI

---

## 🧾 Licença

Distribuído sob a licença Creative Commons BY-NC-SA 4.0. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🔗 Recursos relacionados

📄 Artigo completo: Análise de Dados Criminais em Grafos (UNIFEI, 2025)

📘 Código-fonte e análise: [GitHub Repository](https://github.com/lucas-luiz/grafos_analise_dados_criminais)