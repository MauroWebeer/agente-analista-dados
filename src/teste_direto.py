import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langfuse.callback import CallbackHandler

load_dotenv()

print("Testando envio via LangChain + LangFuse...")

# Inicializa o handler do LangFuse
langfuse_handler = CallbackHandler()

# Inicializa o Groq
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
    max_tokens=100
)

# Invoca o modelo passando o callback explicitamente
resposta = llm.invoke(
    "Responda apenas: Teste de observabilidade OK.",
    config={"callbacks": [langfuse_handler]}
)

print("Resposta do LLM:", resposta.content)
print("Teste concluído. Verifique o painel do LangFuse!")