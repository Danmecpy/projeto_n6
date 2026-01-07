# src/projeto_n6/paths.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from projeto_n6.settings import DATA_DIR, DOMAIN
from projeto_n6.run_context import RunContext


@dataclass(frozen=True)
class PipelinePaths:
    """
    Caminhos de entrada/saída para 1 execução (RunContext).
    """
    run_partition: str

    silver_dir: Path
    rejects_dir: Path
    metrics_dir: Path
    logs_dir: Path  # ✅ ADICIONADO

    def silver_file(self, name: str) -> Path:
        return self.silver_dir / f"{name}.parquet"

    def rejects_file(self, name: str) -> Path:
        return self.rejects_dir / f"{name}_rejects.parquet"

    def metrics_file(self, name: str = "metrics") -> Path:
        return self.metrics_dir / f"{name}.parquet"

    def log_file(self, name: str = "pipeline") -> Path:
        return self.logs_dir / f"{name}.log"


def build_paths(ctx: RunContext) -> PipelinePaths:
    """
    Monta a estrutura com particionamento: run_date=YYYY-MM-DD
    """
    run_partition = f"run_date={ctx.run_date.isoformat()}"

    silver_dir = DATA_DIR / "silver" / DOMAIN / run_partition
    rejects_dir = DATA_DIR / "rejects" / DOMAIN / run_partition
    metrics_dir = DATA_DIR / "metrics" / DOMAIN / run_partition

    logs_dir = Path("logs") / DOMAIN / run_partition  # ✅ FORA do DATA_DIR

    return PipelinePaths(
        run_partition=run_partition,
        silver_dir=silver_dir,
        rejects_dir=rejects_dir,
        metrics_dir=metrics_dir,
        logs_dir=logs_dir,
    )


def ensure_run_dirs(paths: PipelinePaths) -> None:
    """
    Garante que as pastas existem antes de escrever arquivos.
    """
    paths.silver_dir.mkdir(parents=True, exist_ok=True)
    paths.rejects_dir.mkdir(parents=True, exist_ok=True)
    paths.metrics_dir.mkdir(parents=True, exist_ok=True)
    paths.logs_dir.mkdir(parents=True, exist_ok=True)  # ✅ ADICIONADO
