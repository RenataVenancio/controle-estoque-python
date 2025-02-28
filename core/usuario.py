from dataclasses import dataclass

@dataclass
class Usuario:
    id: int
    nome: str
    usuario: str
    senha: str        
    perfil: str # Se é perfil Admin ou Comun

    def e_admin(self) -> bool:
        return self.perfil == "admin"