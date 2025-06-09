import pandas as pd

def carregar_e_limpar_dados(caminho_csv):
    df = pd.read_csv(caminho_csv, sep=';', low_memory=False)

    df = df[["Date Rptd", "AREA NAME", "Crm Cd Desc", "Mocodes", "LAT", "LON"]].copy()
    df.dropna(subset=["Date Rptd", "AREA NAME", "Crm Cd Desc"], inplace=True)

    df['Date Rptd'] = pd.to_datetime(df['Date Rptd'], errors='coerce')
    df.dropna(subset=["Date Rptd"], inplace=True)
    df["Mocodes"] = df["Mocodes"].fillna("0000")

    df.reset_index(drop=True, inplace=True)

    return df
