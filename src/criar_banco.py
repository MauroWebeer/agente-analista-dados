import os
import duckdb

# Garante que a pasta data/ existe
os.makedirs("data", exist_ok=True)

# Caminho para o banco DuckDB
db_path = "data/dados_empresa.duckdb"

print(f"Conectando ao DuckDB em: {db_path}")
conn = duckdb.connect(db_path)

# Dropando as tabelas na ordem correta (filha primeiro, depois os pais)
conn.execute("DROP TABLE IF EXISTS vendas;")
conn.execute("DROP TABLE IF EXISTS clientes;")
conn.execute("DROP TABLE IF EXISTS produtos;")

# Criando a tabela de Clientes
conn.execute("""
    CREATE TABLE clientes (
        cliente_id INTEGER PRIMARY KEY,
        nome VARCHAR,
        segmento VARCHAR,
        cidade VARCHAR,
        estado VARCHAR
    )
""")

# Criando a tabela de Produtos
conn.execute("""
    CREATE TABLE produtos (
        produto_id INTEGER PRIMARY KEY,
        nome_produto VARCHAR,
        categoria VARCHAR,
        preco_unitario DECIMAL(10, 2)
    )
""")

# Criando a tabela de Vendas (Fatos)
conn.execute("""
    CREATE TABLE vendas (
        venda_id INTEGER PRIMARY KEY,
        data_venda DATE,
        cliente_id INTEGER,
        produto_id INTEGER,
        quantidade INTEGER,
        valor_total DECIMAL(10, 2),
        FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id),
        FOREIGN KEY (produto_id) REFERENCES produtos(produto_id)
    )
""")

print("Tabelas criadas com sucesso! Inserindo dados sintéticos...")

# Inserindo dados simulados em Clientes
conn.execute("""
    INSERT INTO clientes VALUES
    (1, 'TechCorp Soluções', 'Corporativo', 'São Paulo', 'SP'),
    (2, 'Inova Varejo Ltda', 'Varejo', 'Rio de Janeiro', 'RJ'),
    (3, 'Agropecuária Vale Verde', 'Agronegócio', 'Ribeirão Preto', 'SP'),
    (4, 'Alpha Logística', 'Logística', 'Curitiba', 'PR'),
    (5, 'Beta Consultoria', 'Serviços', 'Belo Horizonte', 'MG');
""")

# Inserindo dados simulados em Produtos
conn.execute("""
    INSERT INTO produtos VALUES
    (101, 'Servidor Cloud 4vCPU', 'Infraestrutura', 1500.00),
    (102, 'Licença Software ERP (Anual)', 'Software', 12000.00),
    (103, 'Gateway de Pagamento API', 'Software', 450.00),
    (104, 'Consultoria de Dados (Hora)', 'Serviços', 250.00),
    (105, 'Dashboard Analítico BI', 'Software', 3500.00);
""")

# Inserindo dados simulados em Vendas
conn.execute("""
    INSERT INTO vendas VALUES
    (1, '2026-01-15', 1, 101, 2, 3000.00),
    (2, '2026-01-18', 2, 103, 5, 2250.00),
    (3, '2026-02-05', 3, 102, 1, 12000.00),
    (4, '2026-02-10', 1, 104, 10, 2500.00),
    (5, '2026-03-01', 4, 105, 3, 10500.00),
    (6, '2026-03-12', 5, 101, 1, 1500.00),
    (7, '2026-04-02', 2, 102, 2, 24000.00);
""")

# Validação rápida dos dados inseridos
print("\n--- Validação: Total de Vendas por Cliente ---")
resultado = conn.execute("""
    SELECT 
        c.nome AS cliente, 
        SUM(v.valor_total) AS total_vendido
    FROM vendas v
    JOIN clientes c ON v.cliente_id = c.cliente_id
    GROUP BY c.nome
    ORDER BY total_vendido DESC;
""").fetchall()

for linha in resultado:
    print(f"Cliente: {linha[0]} | Total: R$ {linha[1]:.2f}")

conn.close()
print("\nBanco DuckDB configurado e populado com sucesso!")