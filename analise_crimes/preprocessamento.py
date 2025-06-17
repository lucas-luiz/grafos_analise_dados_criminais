import pandas as pd

def carregar_e_limpar_dados(caminho_csv):
    """
    Função responsável por carregar o dataset a partir de um arquivo CSV
    e realizar a limpeza inicial dos dados.

    Parâmetros:
        caminho_csv (str): Caminho para o arquivo CSV contendo os dados.

    Retorno:
        df (DataFrame): DataFrame Pandas contendo apenas as colunas relevantes,
                        com datas convertidas e valores nulos removidos.
    """

    df = pd.read_csv(caminho_csv, sep=';', low_memory=False)
    df = df[["DATE OCC", "AREA NAME", "Crm Cd Desc", "Mocodes"]].copy() # Mantém apenas as colunas de interesse
    df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], errors='coerce')
    df.dropna(subset=["DATE OCC", "AREA NAME", "Crm Cd Desc", "Mocodes"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df