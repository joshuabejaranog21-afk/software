from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
# import schemas
from database import get_db, engine
from auth import verify_token, get_password_hash, verify_password, create_access_token
from datetime import timedelta

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Agenda", version="1.0.0")

# Configurar CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL de tu frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schemas (estructuras de datos)
from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    email: str
    password: str
    nombre: str
    rol: str = "user"

class UserResponse(BaseModel):
    id: int
    email: str
    nombre: str
    rol: str

    class Config:
        from_attributes = True

class ContactoCreate(BaseModel):
    nombre: str
    email: Optional[str] = None
    telefono: Optional[str] = None

class ContactoResponse(BaseModel):
    id: int
    nombre: str
    email: Optional[str]
    telefono: Optional[str]
    usuario_id: int

    class Config:
        from_attributes = True
        
@app.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.email == user_data.email).first()
    print("Usuario encontrado:", user)  # 👈 agrega esto

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    print("Verificando contraseña...")  # 👈 agrega esto
    if not verify_password(user_data.password, user.password):
        print("Contraseña incorrecta")  # 👈 agrega esto
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    access_token = create_access_token(
        data={"sub": user.email, "id": user.id, "rol": user.rol},
        expires_delta=timedelta(minutes=30)
    )

    print("Token generado correctamente:", access_token[:20])  # 👈 agrega esto

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "nombre": user.nombre,
            "rol": user.rol
        }
    }

# Rutas de Usuarios (solo admin)
@app.get("/usuarios", response_model=List[UserResponse])
def get_usuarios(token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    if token.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    
    usuarios = db.query(models.Usuario).all()
    return usuarios

@app.post("/usuarios", response_model=UserResponse)
def crear_usuario(usuario: UserCreate, token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    if token.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    
    # Verificar si el email ya existe
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Crear nuevo usuario
    db_usuario = models.Usuario(
        email=usuario.email,
        password=get_password_hash(usuario.password),
        nombre=usuario.nombre,
        rol=usuario.rol
    )
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    
    return db_usuario

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    if token.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    
    if usuario_id == token.get("id"):
        raise HTTPException(status_code=400, detail="No puedes eliminarte a ti mismo")
    
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    
    return {"message": "Usuario eliminado correctamente"}

# Rutas de Contactos (Agenda)
@app.get("/contactos", response_model=List[ContactoResponse])
def get_contactos(token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    contactos = db.query(models.Contacto).filter(models.Contacto.usuario_id == token.get("id")).all()
    return contactos

@app.post("/contactos", response_model=ContactoResponse)
def crear_contacto(contacto: ContactoCreate, token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    db_contacto = models.Contacto(
        nombre=contacto.nombre,
        email=contacto.email,
        telefono=contacto.telefono,
        usuario_id=token.get("id")
    )
    
    db.add(db_contacto)
    db.commit()
    db.refresh(db_contacto)
    
    return db_contacto

@app.put("/contactos/{contacto_id}", response_model=ContactoResponse)
def actualizar_contacto(contacto_id: int, contacto: ContactoCreate, token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    db_contacto = db.query(models.Contacto).filter(
        models.Contacto.id == contacto_id, 
        models.Contacto.usuario_id == token.get("id")
    ).first()
    
    if not db_contacto:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    
    db_contacto.nombre = contacto.nombre
    db_contacto.email = contacto.email
    db_contacto.telefono = contacto.telefono
    
    db.commit()
    db.refresh(db_contacto)
    
    return db_contacto

@app.delete("/contactos/{contacto_id}")
def eliminar_contacto(contacto_id: int, token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    contacto = db.query(models.Contacto).filter(
        models.Contacto.id == contacto_id, 
        models.Contacto.usuario_id == token.get("id")
    ).first()
    
    if not contacto:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    
    db.delete(contacto)
    db.commit()
    
    return {"message": "Contacto eliminado correctamente"}

# Ruta para verificar el token
@app.get("/verify-token")
def verify_token_route(token: dict = Depends(verify_token)):
    return {"valid": True, "user": token}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
