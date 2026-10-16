import os
from langchain_community.utilities import SQLDatabase

def obter_conexao_sql() -> SQLDatabase:
    """
    Retorna a instância do SQLDatabase do LangChain conectada ao DuckDB local.
    Isso permite que o agente inspecione o esquema das tabelas automaticamente.
    """
    db_path = "data/dados_empresa.duckdb"
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Banco de dados não encontrado em {db_path}. Execute 'src/criar_banco.py' primeiro.")

    # String de conexão do DuckDB via SQLAlchemy / duckdb-engine
    uri_conexao = f"duckdb:///{db_path}"
    
    # Inicializa o utilitário SQLDatabase do LangChain
    db = SQLDatabase.from_uri(uri_conexao)
    return db

if __name__ == "__main__":
    print("Testando conexão do LangChain com o DuckDB...")
    db = obter_conexao_sql()
    
    print("\n--- Metadados detectados pelo LangChain ---")
    print(f"Tabelas disponíveis: {db.get_usable_table_names()}")
    print("\nInformações detalhadas do esquema:")
    print(db.get_table_info())