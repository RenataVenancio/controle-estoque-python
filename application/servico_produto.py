from typing import List
from core.produto import Produto
from core.repositorio import RepositorioProduto

class ServicoProduto:
    def __init__(self, repositorio: RepositorioProduto):
        self.repositorio = repositorio

    def adicionar_produto(self, nome: str, quantidade: int, preco: float, estoque_minimo: int):
        produto = Produto(nome, quantidade, preco, estoque_minimo)
        self.repositorio.adicionar(produto)
        return "Produto adicionado com sucesso!"
    
    def buscar_produto(self, id: int) -> Produto:
        return self.repositorio.buscar_produto(id)
    
    def listar_produtos(self) -> List[Produto]:
        return self.repositorio.listar()
    
    def atualizar_produto(self, produto: Produto) -> str:
        self.repositorio.atualizar(produto)
        return "Produto atualizado com sucesso!"
    
    def remover_produto(self, id: int) -> str:
        self.repositorio.remover(id)