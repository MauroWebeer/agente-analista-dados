import os
from dotenv import load_dotenv
from llm import obter_llm
from db import obter_conexao_sql
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langfuse.callback import CallbackHandler

# Carrega as variáveis de ambiente (incluindo LangFuse e Groq)
load_dotenv()

def criar_agente_analista():
    """
    Cria e configura o Agente Text-to-SQL utilizando o Groq (LLM) 
    e o SQLDatabaseToolkit (LangChain), integrado com LangFuse para observabilidade.
    """
    # 1. Carrega o LLM otimizado
    llm = obter_llm(temperatura=0.0)
    
    # 2. Carrega a conexão com o banco DuckDB
    db = obter_conexao_sql()
    
    # 3. Inicializa o callback do LangFuse para auditoria e tracing
    langfuse_handler = CallbackHandler()
    
    # 4. Cria o Agente SQL
    agente = create_sql_agent(
        llm=llm,
        db=db,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agente, langfuse_handler

if __name__ == "__main__":
    print("Inicializando Agente Analista de Dados com Observabilidade LangFuse...")
    agente, langfuse_handler = criar_agente_analista()
    
    # Pergunta de teste para o nosso Agente
    pergunta = "Qual é o cliente que tem o maior valor total de vendas acumulado?"
    
    print(f"\n--- Pergunta do Analista: {pergunta} ---")
    
    # Passamos o langfuse_handler no parâmetro config para rastrear a execução
    resposta = agente.invoke(
        {"input": pergunta},
        config={"callbacks": [langfuse_handler]}
    )
    
    print("\n--- Resposta Final do Agente ---")
    print(resposta.get("output"))