from dataclasses import dataclass

@dataclass
class Log:
    id: int
    usuario: str
    acao: str
    data_hora: str
