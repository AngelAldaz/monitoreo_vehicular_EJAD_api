from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import PALABRA_SECRETA
from app.database import create_tables
from app.models.rolesModel import Role 
from app.models.brandsModel import Brand
from app.models.modelsModel import Model
from app.models.descriptionsModel import Description

app = FastAPI()

# Llama a la función al iniciar
create_tables()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.get("/")
def root():
  return {"message": "Hello World"}

@app.get("/secreto")
def secreto():
  return {"message": PALABRA_SECRETA}