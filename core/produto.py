from dataclasses import dataclass

@dataclass
class Produto:
    id: int
    nome: str
    quantidade: int
    preco: float
    estoque_minimo: int

    def verificar_estoque_baixo(self) -> bool:
        return self.quantidade < self.estoque_minimo