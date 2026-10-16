import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("A variável GROQ_API_KEY não foi encontrada no arquivo .env!")

print("Chave de API do Groq carregada com sucesso!")

# Inicializando o modelo disponível na sua conta
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0
)

# Testando uma chamada simples
resposta = llm.invoke("Responda apenas: A conexao com o Groq esta funcionando perfeitamente!")
print("\n--- Resposta do LLM ---")
print(resposta.content)