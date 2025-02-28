from core.repositorio import RepositorioProduto
from core.produto import Produto
from infra.banco import conectar
from typing import List


class RepositorioProdutoSQLite(RepositorioProduto):
    
    def adicionar(self, produto):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, quantidade, preco, estoque_minimo) VALUES (?, ?, ?, ?)",
                       (produto.nome, produto.quantidade, produto.preco, produto.estoque_minimo))
        conn.commit()
        conn.close()

    def buscar_produto(self, termo):
        conn = conectar()
        cursor = conn.cursor()

        # Determinar se o termo é um número (busca por ID) ou texto (busca por Nome)
        try:
            termo = int(termo)
            comando = "SELECT * FROM produtos WHERE id = ?"
            cursor.execute(comando, (termo,))
        except ValueError:
            comando = "SELECT * FROM produtos WHERE nome LIKE ?"
            cursor.execute(comando, (f"%{termo}%",))

        resultados = cursor.fetchall()
        conn.close()

        return [Produto(id=row[0], nome=row[1], quantidade=row[2], preco=row[3], estoque_minimo=row[4]) for row in resultados]
    
    def listar(self):
        conn = conectar()
        cursor = conn.cursor()
        comando = "SELECT * FROM produtos"
        cursor.execute(comando)
        linhas = cursor.fetchall()
        conn.close()
        produtos = []
        if linhas:
            for linha in linhas:
                produtos.append(Produto(id=linha[0], nome=linha[1], quantidade=linha[2], preco=linha[3], estoque_minimo=linha[4]))
        return produtos
    
    def atualizar(self, produto):
        conn = conectar()
        cursor = conn.cursor()
        comando = '''UPDATE produtos SET nome = ?, quantidade = ?, preco = ?, estoque_minimo = ? WHERE id = ?'''
        cursor.execute(comando,(produto.nome, produto.quantidade, produto.preco, produto.estoque_minimo, produto.id))
        conn.commit()
        conn.close()

    def remover(self, id):
        conn = conectar()
        cursor = conn.cursor()
        comando = "DELETE FROM produtos WHERE id = ?"
        cursor.execute(comando,(id,))
        conn.commit()
        conn.close()

    def contar_total_produtos(self):
        
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM produtos")
        total = cursor.fetchone()[0]
        cursor.close()
        return total
    
    def contar_estoque_baixo(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM produtos WHERE quantidade < estoque_minimo")
        estoque_baixo = cursor.fetchone()[0]
        cursor.close()
        return estoque_baixo
    
    def calcular_valor_total_estoque(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(quantidade * preco) FROM produtos")
        valor_total = cursor.fetchone()[0]
        cursor.close()
        return valor_total
