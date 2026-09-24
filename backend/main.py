from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db, engine
import models
import hashing

# Como medida de seguridad, aseguramos que las tablas existan al arrancar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PatchProof API", description="API para el MVP de PatchProof (GOYA HACK 2026)")

# Configuracion de CORS: Indispensable para que el frontend en React pueda hacer peticiones
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitimos cualquier origen para agilizar el desarrollo del MVP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {
        "status": "online", 
        "message": "PatchProof API funcionando. Visita /docs para ver los endpoints."
    }

# ==============================================================================
# ESPACIO PARA PERSONA 1 (BACKEND)
# A partir de aqui, la Persona 1 programara los endpoints (GET/POST /bounties, etc.)
# Ejemplo de uso de la base de datos inyectada:
#
# @app.get("/bounties")
# def get_bounties(db: Session = Depends(get_db)):
#     return db.query(models.Bounty).all()
# ==============================================================================