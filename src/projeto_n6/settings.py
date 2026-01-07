
from __future__ import annotations

from pathlib import Path

# Raiz do projeto:
# parents[2] sobe: projeto_n6/settings.py -> projeto_n6 -> src -> <raiz do repo>
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

# Nome do domínio/dataset (para ficar organizado se você tiver mais no futuro)
DOMAIN = "olist"
