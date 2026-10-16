import os
from llm import obter_llm
from db import obter_conexao_sql
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType

def criar_agente_analista():
    """
    Cria e configura o Agente Text-to-SQL utilizando o Groq (LLM) 
    e o SQLDatabaseToolkit (LangChain).
    """
    # 1. Carrega o LLM otimizado (Temperatura 0 para evitar alucinações em SQL)
    llm = obter_llm(temperatura=0.0)
    
    # 2. Carrega a conexão com o banco DuckDB
    db = obter_conexao_sql()
    
    # 3. Inicializa o Toolkit SQL do LangChain
    # Ele entrega ferramentas prontas para o agente: listar tabelas, checar esquemas, rodar queries, etc.
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    # 4. Cria o Agente SQL usando a estratégia de ferramentas estruturadas (OPENAI_FUNCTIONS ou ZERO_SHOT)
    agente = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,  # Mostra no console o passo a passo de raciocínio do agente (ótimo para debug)
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True # Lida com eventuais erros de formatação do LLM graciosamente
    )
    
    return agente

if __name__ == "__main__":
    print("Inicializando Agente Analista de Dados...")
    agente = criar_agente_analista()
    
    # Pergunta de teste para o nosso Agente Text-to-SQL
    pergunta = "Qual é o cliente que tem o maior valor total de vendas acumulado?"
    
    print(f"\n--- Pergunta do Analista: {pergunta} ---")
    resposta = agente.invoke({"input": pergunta})
    
    print("\n--- Resposta Final do Agente ---")
    print(resposta.get("output"))