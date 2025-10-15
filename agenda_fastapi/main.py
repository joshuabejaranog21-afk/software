from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title="API Agenda de Contactos",
    description="Una API REST para gestionar una agenda de contactos",
    version="1.0.0"
)

# Raíz
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Agenda de Contactos"}

# CREATE - Crear nueva persona
@app.post("/personas/", response_model=schemas.Persona, status_code=status.HTTP_201_CREATED)
def crear_persona(persona: schemas.PersonaCreate, db: Session = Depends(get_db)):
    try:
        return crud.crear_persona(db=db, persona=persona)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# READ - Obtener todas las personas
@app.get("/personas/", response_model=List[schemas.Persona])
def leer_personas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    personas = crud.obtener_personas(db, skip=skip, limit=limit)
    return personas

# READ - Obtener persona por ID
@app.get("/personas/{persona_id}", response_model=schemas.Persona)
def leer_persona(persona_id: int, db: Session = Depends(get_db)):
    db_persona = crud.obtener_persona(db, persona_id=persona_id)
    if db_persona is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada"
        )
    return db_persona

# UPDATE - Actualizar persona
@app.put("/personas/{persona_id}", response_model=schemas.Persona)
def actualizar_persona(persona_id: int, persona: schemas.PersonaUpdate, db: Session = Depends(get_db)):
    db_persona = crud.actualizar_persona(db, persona_id=persona_id, persona=persona)
    if db_persona is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada"
        )
    return db_persona

# DELETE - Eliminar persona
@app.delete("/personas/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_persona(persona_id: int, db: Session = Depends(get_db)):
    db_persona = crud.eliminar_persona(db, persona_id=persona_id)
    if db_persona is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada"
        )
    return None

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API funcionando correctamente"}

# Ejecutar la aplicación
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)