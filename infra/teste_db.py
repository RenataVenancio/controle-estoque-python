# from core.produto import Produto
import sqlite3


conn = sqlite3.connect("estoque.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(produtos);")
colunas = cursor.fetchall()

for coluna in colunas:
    print(coluna)

# cursor.execute("drop table usuarios;")
# cursor.execute("drop table produtos;")
# cursor.execute("drop table logs;")

cursor.execute("SELECT SUM(quantidade * preco) FROM produtos")
valor_total = cursor.fetchone()[0]

comando = "SELECT * FROM produtos"
cursor.execute(comando)
linhas = cursor.fetchall()
conn.close()
produtos = []
# if linhas:
#     for linha in linhas:
#         produtos.append(Produto(id=linha[0], nome=linha[1], quantidade=linha[2], preco=linha[3], estoque_minimo=linha[4]))
# # return produtos

conn.close()