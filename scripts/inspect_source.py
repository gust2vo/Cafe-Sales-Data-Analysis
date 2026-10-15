
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"


def main():
    files = list(RAW_DIR.glob("*.csv"))

    if not files:
        raise FileNotFoundError(
            "Nenhum arquivo CSV encontrado em data/raw"
        )

    file = files[0]
    df = pd.read_csv(file)

    print(f"Arquivo: {file.name}")
    print(f"Linhas: {df.shape[0]}")
    print(f"Colunas: {df.shape[1]}")

    print("\nColunas:")
    for column in df.columns:
        print(f"- {column}")

    print("\nPrimeiras 5 linhas:")
    print(df.head())

    print("\nTipos identificados pelo Python:")
    print(df.dtypes)

    print("\nValores nulos:")
    print(df.isnull().sum())


if __name__ == "__main__":
    main()
