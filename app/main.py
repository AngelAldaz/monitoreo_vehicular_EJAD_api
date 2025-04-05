from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import PALABRA_SECRETA
from app.database import create_tables

from app.routers import roleRoutes


app = FastAPI()
app.include_router(roleRoutes.router)

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