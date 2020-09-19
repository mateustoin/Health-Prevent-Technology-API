from datetime import date
from pydantic import BaseModel

class Cliente(BaseModel):
    id: int
    nome: str
    idade: int
    numero_telefone: str 
    endereco: str 
    cep: str 
    doenca: str 
    contato_emergencia: str 
    data_ultima_consulta: date 
    especialidade_medico: str
    status: int

    class Config:
        orm_mode = True