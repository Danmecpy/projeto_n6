# src/projeto_n6/run_context.py
from __future__ import annotations#serve para permitir anotações de tipo futuras

from dataclasses import dataclass ## Added dataclass import serve para criar classes imutáveis e com menos boilerplate
from datetime import datetime, date ## Added date import serve para manipular datas
from uuid import uuid4 ## Added uuid4 import serve para gerar IDs únicos


@dataclass(frozen=True) # serve para criar uma classe imutável 
class RunContext: #criado para representar o contexto de execução do pipeline
    """ 
    Representa 1 execução do pipeline.

    run_date: usado para particionar pastas (run_date=YYYY-MM-DD)
    run_id: identificador único (bom para logs, metrics e auditoria)
    run_ts: timestamp completo da execução
    """
    run_date: date
    run_id: str #serve para armazenar o identificador único da execução
    run_ts: datetime #serve para armazenar o timestamp completo da execução quando o pipeline foi executado 


def new_run_context(run_date: date | None = None) -> RunContext: ##criado para criar um novo contexto de execução
    """
    Cria um contexto novo.
    - Se run_date não for informado, usa a data de hoje.
    """
    rd = run_date or date.today()
    return RunContext(
        run_date=rd,
        run_id=str(uuid4()),
        run_ts=datetime.now(),
    )
