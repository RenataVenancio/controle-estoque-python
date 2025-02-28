from dataclasses import dataclass
from typing import Optional

@dataclass
class Produto:    
    nome: str
    quantidade: int
    preco: float
    estoque_minimo: int
    id: Optional[int] = None

    def verificar_estoque_baixo(self) -> bool:
        return self.quantidade < self.estoque_minimo