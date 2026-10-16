# 🤖 Agente Analista de Dados (Text-to-SQL Inteligente)

Agente inteligente construído em Python que permite a analistas de dados fazerem perguntas em linguagem natural e receberem respostas consolidadas de um banco de dados relacional sem escrever SQL manualmente.

## 🛠️ Stack Tecnológica
- **Linguagem:** Python 3.12
- **Orquestração & Agente:** LangChain & LangChain Community
- **LLM:** Qwen 27B via Groq API (Inferência de alta velocidade)
- **Motor de Computação/Dados:** DuckDB (Banco de dados analítico local e embutido)
- **Observabilidade:** LangFuse (Tracing, métricas e auditoria de queries)

---

## 📂 Estrutura do Projeto
```text
agente-analista-dados/
├── data/
│   └── dados_empresa.duckdb   # Banco DuckDB local simulado
├── src/
│   ├── __init__.py
│   ├── agente.py              # Configuração e execução do Agente ReAct
│   ├── db.py                  # Conexão SQLDatabase do LangChain com DuckDB
│   ├── llm.py                 # Inicialização centralizada do ChatGroq
│   └── criar_banco.py         # Script idempotente de carga inicial das tabelas
├── .env                       # Variáveis de ambiente (Chaves de API)
├── .gitignore
├── requirements.txt           # Dependências fixadas do projeto
└── README.md
```
---

## ⚙️ Como Rodar o Projeto

### 1. Clonar o Repositório
```bash
git clone []
cd agente-analista-dados

```

### 2. Configurar o Ambiente Virtual e Dependências

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

```

### 3. Configurar as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto baseado nas suas chaves:

```env
GROQ_API_KEY=sua_chave_groq_aqui

LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_HOST=[https://us.cloud.langfuse.com](https://us.cloud.langfuse.com)

```

### 4. Inicializar o Banco de Dados DuckDB

Execute o script de criação e carga das tabelas sintéticas (`clientes`, `produtos`, `vendas`):

```bash
python src/criar_banco.py

```

### 5. Executar o Agente Text-to-SQL

Faça uma pergunta em linguagem natural para testar o agente:

```bash
python -m src.agente

```

---

## 🏗️ Arquitetura e Fluxo dos Recursos

```text
 [ Analista de Dados ] 
         │  (Linguagem Natural: "Qual o cliente com maior venda?")
         ▼
 ┌──────────────────────────────────────────────┐
 │              LangChain Agent                 │
 │       (Padrão ReAct + SQL Toolkit)           │
 └──────────────────────┬───────────────────────┘
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
 ┌──────────────┐              ┌──────────────────────────────┐
 │  ChatGroq    │              │          LangFuse            │
 │ (LLM Qwen)   │              │ (Observabilidade & Tracing)  │
 └──────────────┘              └──────────────────────────────┘
         │
         │ (Gera e valida query SQL)
         ▼
 ┌──────────────────────────────────────────────┐
 │               DuckDB Local                   │
 │   (Executa query otimizada nas tabelas)      │
 └──────────────────────────────────────────────┘

```

### 📝 Descrição dos Componentes:

1. **LangChain (`create_sql_agent` & `SQLDatabaseToolkit`):** Atua como o maestro do fluxo. Lê automaticamente os metadados do banco, decide quando inspecionar o esquema, formula a query SQL, valida erros sintáticos e traduz o resultado bruto de volta para linguagem natural.
2. **Groq (`ChatGroq` / Qwen 27B):** O motor de inferência de linguagem. Processa o raciocínio em etapas (ReAct) com alta velocidade de entrega de tokens e restrição rigorosa de temperatura (`0.0`) para evitar alucinações em códigos SQL.
3. **DuckDB (`dados_empresa.duckdb`):** O data warehouse analítico embutido. Processa a query SQL gerada pelo agente de forma extremamente eficiente diretamente no arquivo local.
4. **LangFuse (`CallbackHandler`):** A camada de governança e engenharia. Intercepta todas as chamadas via callback assíncrono e registra no painel da nuvem o custo de tokens, latência de ponta a ponta, o prompt enviado e a query executada.