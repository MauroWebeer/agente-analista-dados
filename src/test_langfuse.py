import os
from dotenv import load_dotenv
from langfuse import Langfuse

# Carrega as variáveis do arquivo .env
load_dotenv()

print("Testando conexão com o LangFuse em:", os.getenv("LANGFUSE_HOST"))

# Inicializa o cliente LangFuse explicitamente com as credenciais do .env
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# Cria um trace de teste simulado
trace = langfuse.trace(
    name="teste-conexao-us",
    input="Teste de regiao US",
    output="Sucesso total na conexao!"
)

# Força o envio imediato para o servidor do LangFuse
langfuse.flush()
print("Trace de teste enviado com sucesso para o LangFuse!")