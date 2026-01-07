# src/projeto_n6/init_run.py
from __future__ import annotations

from projeto_n6.run_context import new_run_context #  serve para criar um novo contexto de execução
from projeto_n6.paths import build_paths, ensure_run_dirs #  serve para garantir que as pastas de saída existem antes de escrever os arquivos


def main() -> None: # Função principal para inicializar uma nova execução do pipeline
    ctx = new_run_context() # Cria um novo contexto de execução com a data de hoje
    paths = build_paths(ctx) # Constrói os caminhos de entrada/saída com base no contexto de execução
    ensure_run_dirs(paths) # Garante que as pastas de saída existem antes de escrever os arquivos

    print("✅ Run criado")
    print(f"run_date: {ctx.run_date}") # Exibe a data da execução
    print(f"run_id:   {ctx.run_id}") # Exibe o identificador único da execução
    print("silver:", paths.silver_dir) # Exibe o caminho da pasta silver
    print("rejects:", paths.rejects_dir) # Exibe o caminho da pasta rejects
    print("metrics:", paths.metrics_dir) # Exibe o caminho da pasta metrics


if __name__ == "__main__":  # Executa a função principal se o script for executado diretamente
    main()
