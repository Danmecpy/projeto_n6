# src/projeto_n6/paths.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path # serve para manipular caminhos de arquivos e pastas de forma independente do sistema operacional

from projeto_n6.settings import DATA_DIR, DOMAIN 
from projeto_n6.run_context import RunContext


@dataclass(frozen=True)
class PipelinePaths: 
    """
    Caminhos de entrada/saída para 1 execução (RunContext).
    """
    run_partition: str ## serve para armazenar a partição de execução no formato run_date=YYYY-MM-DD

    silver_dir: Path
    rejects_dir: Path
    metrics_dir: Path

    def silver_file(self, name: str) -> Path: ## serve para obter o caminho do arquivo Parquet na pasta silver(-> Path é o tipo de retorno da função)
        return self.silver_dir / f"{name}.parquet" ## retorna o caminho completo do arquivo Parquet na pasta silver 

    def rejects_file(self, name: str) -> Path:
        return self.rejects_dir / f"{name}_rejects.parquet"

    def metrics_file(self, name: str = "metrics") -> Path:
        return self.metrics_dir / f"{name}.parquet"


def build_paths(ctx: RunContext) -> PipelinePaths: ## serve para construir os caminhos de entrada/saída com base no contexto de execução
    """
    Monta a estrutura com particionamento: run_date=YYYY-MM-DD
    """
    run_partition = f"run_date={ctx.run_date.isoformat()}"

    silver_dir = DATA_DIR / "silver" / DOMAIN / run_partition
    rejects_dir = DATA_DIR / "rejects" / DOMAIN / run_partition
    metrics_dir = DATA_DIR / "metrics" / DOMAIN / run_partition

    return PipelinePaths(
        run_partition=run_partition,
        silver_dir=silver_dir,
        rejects_dir=rejects_dir,
        metrics_dir=metrics_dir,
    )


def ensure_run_dirs(paths: PipelinePaths) -> None: ## serve para garantir que as pastas de saída existem antes de escrever os arquivos
    """
    Garante que as pastas existem antes de escrever Parquet.
    """
    paths.silver_dir.mkdir(parents=True, exist_ok=True)
    paths.rejects_dir.mkdir(parents=True, exist_ok=True)
    paths.metrics_dir.mkdir(parents=True, exist_ok=True)
