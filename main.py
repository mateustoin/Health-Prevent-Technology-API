import requests
from totalvoice.cliente import Cliente

from typing import List

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

# Criando base para os requests de envio de mensagens
def envia_mensagem(numero, mensagem):
    headers = {
        'Content-Type': 'application/json',
        'Access-Token': 'b9f0bbbca94a96afbdac456f5ec2658b'
    }
    
    json = {
        "numero_destino": numero,
		"mensagem": mensagem
    }
    url = 'https://api2.totalvoice.com.br/sms'
    requests.post(url, headers = headers, data=json)

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.get("/clientes/", response_model=List[schemas.Client])
def show_records(db: Session = Depends(get_db)):
    records = db.query(models.Client).all()
    return records

@app.get("/clientes/doenca/{tipo_doenca}", response_model=List[schemas.Client])
def retorna_pela_doenca(tipo_doenca: str, db: Session = Depends(get_db)):
    records = db.query(models.Client).filter_by(doenca=tipo_doenca).all()
    return records

@app.get("/clientes/idade/{min}/{max}", response_model=List[schemas.Client])
def retorna_intervalo_idade(min: int, max: int, db: Session = Depends(get_db)):
    records = db.query(models.Client).filter(models.Client.idade >= min)
    records = records.filter(models.Client.idade <= max).all()
    
    return records

@app.get("/clientes/idade/menor/{idade}", response_model=List[schemas.Client])
def retorna_menorque_idade(idade: int, db: Session = Depends(get_db)):
    records = db.query(models.Client).filter(models.Client.idade <= idade).all()
    
    return records

@app.get("/clientes/idade/maior/{idade}", response_model=List[schemas.Client])
def retorna_maiorque_idade(idade: int, db: Session = Depends(get_db)):
    records = db.query(models.Client).filter(models.Client.idade >= idade).all()
    
    return records

@app.get("/notification/{tipo_doenca}", response_model=List[schemas.Client])
def spread_notification(tipo_doenca: str, db: Session = Depends(get_db)):
    records = db.query(models.Client).filter_by(doenca=tipo_doenca).all()
    return records
    
@app.get("/notification/sms/doenca/{tipo_doenca}", response_model=List[schemas.Client])
def spread_notification_doenca(tipo_doenca: str, db: Session = Depends(get_db)):
    records = db.query(models.Client).filter_by(doenca=tipo_doenca).all()

    for dados in records:
        sms_client = Cliente('b9f0bbbca94a96afbdac456f5ec2658b', 'https://api2.totalvoice.com.br/sms')
        response = sms_client.sms.enviar(dados.numero_telefone, "Parabéns, você está doente e um dia vai morrer!")

    return records