import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Carrega variáveis do arquivo .env
load_dotenv()

def obter_llm(temperatura: float = 0.0) -> ChatGroq:
    """
    Retorna a instância configurada do ChatGroq para ser utilizada
    nos componentes do LangChain (como o agente Text-to-SQL).
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("A variável GROQ_API_KEY não foi encontrada no arquivo .env!")

    # Instancia o modelo Groq com temperatura 0 para maior determinismo no SQL
    llm = ChatGroq(
        model="qwen/qwen3.8-27b",
        temperature=temperatura,
        api_key=api_key
    )
    
    return llm

if __name__ == "__main__":
    # Teste rápido do módulo
    print("Testando inicialização do LLM via Groq...")
    modelo = obter_llm()
    resposta = modelo.invoke("Responda apenas: Conexao centralizada com o Groq validada com sucesso!")
    print(resposta.content)