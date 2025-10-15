
from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey, Text
from sqlalchemy.sql import func
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    nombre = Column(String(255), nullable=False)
    rol = Column(Enum('admin', 'user'), default='user')
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

class Contacto(Base):
    __tablename__ = "contactos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255))
    telefono = Column(String(20))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
