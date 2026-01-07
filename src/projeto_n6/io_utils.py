from __future__ import annotations

from pathlib import Path
import pandas as pd


def write_parquet(df: pd.DataFrame, path: Path) -> None: ##serve para escrever um DataFrame em formato Parquet
    """
    Escreve DataFrame em Parquet.
    Cria diretórios se necessário.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
