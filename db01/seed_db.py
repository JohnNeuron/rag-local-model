from faker import Faker
import mysql.connector
import random

# Instancia o Faker para dados em pt_BR
fake = Faker('pt_BR')

# Configuração da conexão com o banco de dados
conexao = mysql.connector.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha",  
    database="seu_banco"   
)
cursor = conexao.cursor()

# Criação da tabela estoqueProdutos 
create_table_query = """
CREATE TABLE IF NOT EXISTS estoqueProdutos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto VARCHAR(100),
    quantidade INT,
    preco DECIMAL(10,2),
    data_atualizacao DATE
);
"""

#Realiza a execução da query
cursor.execute(create_table_query)
print("Tabela 'estoqueProdutos' criada ou já existente.")

# Lista de produtos fictícios
produtos = ['Camiseta', 'Calça', 'Tênis', 'Boné', 'Jaqueta', 'Bermuda']

# Número de registros que serão inseridos
num_registros = 10000

for _ in range(num_registros):

    # Escolhe um produto aleatório
    produto = random.choice(produtos)

    # Gera uma quantidade aleatória entre 1 e 100
    quantidade = random.randint(1, 100)

    # Gera um preço aleatório entre 10.0 e 200.0 com duas casas decimais
    preco = round(random.uniform(10.0, 200.0), 2)
    
    # Gera uma data aleatória no último ano
    data_atualizacao = fake.date_between(start_date='-1y', end_date='today')
    
    # Insere os dados na tabela
    insert_query = """
    INSERT INTO estoqueProdutos (produto, quantidade, preco, data_atualizacao)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (produto, quantidade, preco, data_atualizacao))

# Confirma as inserções no banco de dados
conexao.commit()

print(f"{num_registros} registros inseridos com sucesso na tabela estoqueProdutos.")

# Fecha o cursor e a conexão
cursor.close()
conexao.close()
