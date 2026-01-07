from __future__ import annotations

import logging
from pathlib import Path   

def setup_logger(name: str, log_file: Path, ) -> logging.Logger:
    """
    Configura um logger padrão do pipeline.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True) #garante que o diretório do log existe
    logger = logging.getLogger(name) #cria o logger
    logger.setLevel(logging.INFO) #serve para definir o nível de log
    
    #evita logs duplicados em re-runs
    if logger.handlers:
        return logger

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') # formato do log 
    
    #log em arquivo
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    
    #log no console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger