from typing import List
from core.usuario import Usuario
from core.repositorio import RepositorioUsuario

class ServicoUsuario:
    def __init__(self, repositorio: RepositorioUsuario):
        self.repositorio = repositorio

    def autenticar(self, usuario: str, senha: str):
        login = self.repositorio.buscar_por_usuario(usuario)
        return login and self.repositorio.verificar_senha(senha, login.senha)
    
    def buscar_usuario(self, usuario: str) -> Usuario:
        return self.repositorio.buscar_por_usuario(usuario)
    
    def listar_usuario(self) -> List[Usuario]:
        return self.repositorio.listar()
    
    def adicionar_usuario(self, usuario: Usuario):
        # Criptografar a senha antes de usuar
        usuario.senha = self.repositorio.gerar_hash_senha(usuario.senha)
        self.repositorio.adicionar(usuario)

    def atualizar_usuario(self, usuario: Usuario):
        # Se a senha for fornecida, criptografa a nova senha
        if usuario.senha:
            usuario.senha = self.repositorio.gerar_hash_senha(usuario.senha)
        else:
            # Se a senha não for fornecida, mantém a senha atual
            usuario_atual = self.repositorio.buscar_por_usuario(usuario.usuario)
            if usuario_atual:
                usuario.senha = usuario_atual.senha
        
        self.repositorio.atualizar(usuario)

    def remover_usuario(self, id: int):
        self.repositorio.remover(id)