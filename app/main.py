from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import PALABRA_SECRETA
from app.database import create_tables
from app.routers import vehicleRoutes


from app.routers import roleRoutes, brandRoutes, modelRoutes, descriptionRoutes, userRoutes, maintenanceRoutes, routeRoutes

app = FastAPI()
app.include_router(brandRoutes.router)
app.include_router(modelRoutes.router)
app.include_router(descriptionRoutes.router)
app.include_router(vehicleRoutes.router)
app.include_router(roleRoutes.router)
app.include_router(userRoutes.router) 
app.include_router(maintenanceRoutes.router)
app.include_router(routeRoutes.router)
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