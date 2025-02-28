from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    nome: str
    usuario: str
    senha: str        
    perfil: str # Se é perfil Admin ou Comun
    id: Optional[int] = None


    def e_admin(self) -> bool:
        return self.perfil == "admin"