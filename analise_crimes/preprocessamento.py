import pandas as pd

def carregar_e_limpar_dados(caminho_csv):
    df = pd.read_csv(caminho_csv, sep=';', low_memory=False)

    df = df[["DATE OCC", "AREA NAME", "Crm Cd Desc", "Mocodes", "LAT", "LON"]].copy()
    df.dropna(subset=["DATE OCC", "AREA NAME", "Crm Cd Desc"], inplace=True)

    df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], errors='coerce')
    df.dropna(subset=["DATE OCC"], inplace=True)
    df["Mocodes"] = df["Mocodes"].fillna("0000")

    df.reset_index(drop=True, inplace=True)
    return df
