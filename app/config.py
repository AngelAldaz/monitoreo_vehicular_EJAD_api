import os
from dotenv import load_dotenv

load_dotenv()

PALABRA_SECRETA = os.getenv("PALABRA", "No encontrado")

DATABASE_URL = os.getenv("DATABASE_URL")