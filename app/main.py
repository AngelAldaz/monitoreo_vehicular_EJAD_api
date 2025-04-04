from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import PALABRA_SECRETA

app = FastAPI()

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