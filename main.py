from totalvoice.cliente import Cliente

from pydantic import BaseModel
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
class Info(BaseModel):
    eventName: str
    minAge: Optional[int] = None
    maxAge: Optional[int] = None
    clinicalCondition: str
    message: str
    company: Optional[str] = None
    
class InfoDisease(BaseModel):
    eventName: str
    clinicalCondition: str
    message: str
    company: str
    
@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.get("/cliente/", response_model=List[schemas.Client])
def show_records(db: Session = Depends(get_db)):
    """Retorna lista de clientes armazenados no banco de dados.
    """
    records = db.query(models.Client).all()
    
    return records

@app.get("/clients/disease/{type_disease}", response_model=List[schemas.Client])
def retorna_por_doenca(type_disease: str, db: Session = Depends(get_db)):
    records = db.query(models.Client).filter_by(doenca=type_disease).all()
    
    return records

@app.get("/clients/age/{min}/{max}", response_model=List[schemas.Client])
def retorna_intervalo_idade(min: int, max: int, db: Session = Depends(get_db)):
    records = db.query(models.Client).filter(models.Client.idade >= min)
    records = records.filter(models.Client.idade <= max).all()
    
    return records

@app.get("/clients/age/min/{idade}", response_model=List[schemas.Client])
def retorna_menor_que_idade(idade: int, db: Session = Depends(get_db)):
    records = db.query(models.Client).filter(models.Client.idade <= idade).all()
    
    return records

@app.get("/clients/age/max/{idade}", response_model=List[schemas.Client])
def retorna_maior_que_idade(idade: int, db: Session = Depends(get_db)):
    records = db.query(models.Client).filter(models.Client.idade >= idade).all()
    
    return records

@app.get("/notification/{tipo_doenca}", response_model=List[schemas.Client])
def spread_notification(tipo_doenca: str, db: Session = Depends(get_db)):
    records = db.query(models.Client).filter_by(doenca=tipo_doenca).all()
    
    return records

# Endpoints com background tasks
def send_sms(numero: str, mensagem: str):
    sms_client = Cliente('b9f0bbbca94a96afbdac456f5ec2658b', 'https://api2.totalvoice.com.br/sms')
    response = sms_client.sms.enviar(numero, mensagem)

@app.get("/notification/sms/doenca/{tipo_doenca}", response_model=List[schemas.Client])
async def spread_notification_doenca(tipo_doenca: str, db: Session = Depends(get_db), background_tasks: BackgroundTasks = BackgroundTasks):
    records = db.query(models.Client).filter_by(doenca=tipo_doenca).all()

    for dados in records:
        background_tasks.add_task(send_sms, dados.numero_telefone, "Parabéns, você está doente e um dia vai morrer!")

    return records

@app.post("/notification/sms/disease/", response_model=List[schemas.Client])
async def spread_notification_body_disease(item: Info, db: Session = Depends(get_db), background_tasks: BackgroundTasks = BackgroundTasks):
    records = db.query(models.Client).filter_by(doenca = item.clinicalCondition).all()

    message = item.eventName + '\n' + item.message
    
    for dados in records:
        background_tasks.add_task(send_sms, dados.numero_telefone, message)

    return records

@app.post("/notification/sms/age/", response_model=List[schemas.Client])
async def spread_notification_body_age(item: Info, db: Session = Depends(get_db), background_tasks: BackgroundTasks = BackgroundTasks):
    records = db.query(models.Client).filter(models.Client.idade >= item.minAge)
    records = records.filter(models.Client.idade <= item.maxAge).all()

    message = item.eventName + ': ' + item.message
    
    for dados in records:
        background_tasks.add_task(send_sms, dados.numero_telefone, message)

    return records