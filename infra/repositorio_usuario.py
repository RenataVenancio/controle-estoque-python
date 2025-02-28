from core.repositorio import RepositorioUsuario
from core.usuario import Usuario
from infra.banco import conectar
from typing import List


class RepositorioUsuarioSQLite(RepositorioUsuario):
    
    def adicionar(self, usuario: Usuario) -> None:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, usuario, senha, perfil) VALUES (?, ?, ?, ?, ?)",
                       (usuario.nome, usuario.usuario, usuario.senha, usuario.perfil))
        conn.commit()
        conn.close()

    def buscar_por_usuario(self, usuario):
        conn = conectar()
        cursor = conn.cursor()
        # comando = "SELECT * FROM usuarios WHERE usuario = {}".format(usuario)
        comando = "SELECT * FROM usuarios WHERE usuario = ?"
        cursor.execute(comando, (usuario,))
        linha = cursor.fetchone()
        conn.close()
        if linha:
            retorno = Usuario(id=linha[0], nome=linha[1], usuario=linha[2], senha=linha[3], perfil=linha[4])
            return retorno
        return None
    
    def listar(self):
        conn = conectar()
        cursor = conn.cursor()
        comando = "SELECT * FROM usuarios"
        cursor.execute(comando)
        linhas = cursor.fetchall()
        conn.close()
        usuarios = []
        if linhas:
            for linha in linhas:
                usuarios.append(Usuario(id=linha[0], nome=linha[1], usuario=linha[2], senha=linha[3], perfil=linha[4]))
        return usuarios
    
    def remover(self, id):
        conn = conectar()
        cursor = conn.cursor()
        comando = "DELETE FROM usuarios WHERE id = ?"
        cursor.execute(comando,(id,))
        conn.commit()
        conn.close()
