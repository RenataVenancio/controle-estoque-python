from abc import ABC, abstractmethod
from typing import List

from core.log import Log
from .produto import Produto
from .usuario import Usuario
import bcrypt

class RepositorioProduto(ABC):
    
    @abstractmethod
    def adicionar(self, produto: Produto) -> None:
        pass

    @abstractmethod
    def buscar_produto(self, id: int) -> Produto:
        pass

    @abstractmethod
    def listar(self) -> List[Produto]:
        pass

    @abstractmethod
    def atualizar(self, produto: Produto) -> None:
        pass

    @abstractmethod
    def remover(self, id: int) -> None:
        pass

class RepositorioUsuario(ABC):

    @abstractmethod
    def adicionar(self, usuario: Usuario) -> None:
        pass

    @abstractmethod
    def buscar_por_usuario(self, usuario: str) -> Usuario:
        pass

    @abstractmethod
    def listar(self) -> List[Usuario]:
        pass

    @abstractmethod
    def remover(self, id: int) -> None:
        pass

    @abstractmethod
    def atualizar(self, usuario: Usuario) -> None:
        pass

    def gerar_hash_senha(self, senha: str):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')
    
    def verificar_senha(self, senha: str, senha_hash: str):
        teste = self.gerar_hash_senha(senha)
        return bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8'))
    
class RepositorioLog(ABC):
    @abstractmethod
    def adicionar(self, log: Log) -> None:
        pass