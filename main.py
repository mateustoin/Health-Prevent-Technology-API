from typing import List

from fastapi import Depends, FastAPI, HTTPException
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

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.get("/clientes/", response_model=List[schemas.Cliente])
def show_records(db: Session = Depends(get_db)):
    records = db.query(models.Cliente).all()
    return records

@app.get("/clientes/doenca/{tipo_doenca}", response_model=List[schemas.Cliente])
def retorna_pela_doenca(tipo_doenca: str, db: Session = Depends(get_db)):
    records = db.query(models.Cliente).filter_by(doenca=tipo_doenca).all()
    return records

@app.get("/clientes/idade/{min}/{max}", response_model=List[schemas.Cliente])
def retorna_intervalo_idade(min: int, max: int, db: Session = Depends(get_db)):
    records = db.query(models.Cliente).filter(models.Cliente.idade >= min)
    records = records.filter(models.Cliente.idade <= max).all()
    
    return records

@app.get("/clientes/idade/menor/{idade}", response_model=List[schemas.Cliente])
def retorna_menorque_idade(idade: int, db: Session = Depends(get_db)):
    records = db.query(models.Cliente).filter(models.Cliente.idade <= idade).all()
    
    return records

@app.get("/clientes/idade/maior/{idade}", response_model=List[schemas.Cliente])
def retorna_maiorque_idade(idade: int, db: Session = Depends(get_db)):
    records = db.query(models.Cliente).filter(models.Cliente.idade >= idade).all()
    
    return records

@app.get("/notification/{tipo_doenca}", response_model=List[schemas.Cliente])
def spread_notification(tipo_doenca: str, db: Session = Depends(get_db)):
    records = db.query(models.Cliente).filter_by(doenca=tipo_doenca).all()
    return records