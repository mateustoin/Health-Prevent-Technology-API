from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.types import Date

from database import Base

class Cliente(Base):
    __tablename__ = "Cliente"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50))
    idade = Column(Integer)
    numero_telefone = Column(String(20))
    endereco = Column(String(100))
    cep = Column(String(12))
    doenca = Column(String(15))
    contato_emergencia = Column(String(20))
    data_ultima_consulta = Column(Date)
    especialidade_medico = Column(String(20))
    status = Column(SmallInteger)