#!/usr/bin/env python3
"""
Script para inicializar la base de datos del sistema de agenda.
"""
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
import models
from database import DATABASE_URL, Base, engine

# Configuración de password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def init_database():
    """Inicializa la base de datos y crea el usuario admin."""
    try:
        print("🔧 Inicializando base de datos...")
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas exitosamente")
        
        # Crear sesión
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Verificar si ya existe el usuario admin
        existing_admin = db.query(models.Usuario).filter(
            models.Usuario.email == "admin@system.com"
        ).first()
        
        if existing_admin:
            print("⚠️  El usuario admin ya existe")
            print(f"   Email: {existing_admin.email}")
            print(f"   Nombre: {existing_admin.nombre}")
            print(f"   Rol: {existing_admin.rol}")
        else:
            # Crear usuario admin
            admin_user = models.Usuario(
                email="admin@system.com",
                password=get_password_hash("admin123"),
                nombre="Administrador",
                rol="admin"
            )
            
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            print("✅ Usuario administrador creado exitosamente:")
            print(f"   Email: admin@system.com")
            print(f"   Password: admin123")
            print(f"   Nombre: Administrador")
            print(f"   Rol: admin")
        
        # Crear algunos usuarios de prueba
        test_users = [
            {
                "email": "usuario1@test.com",
                "password": "password123",
                "nombre": "Usuario Prueba 1",
                "rol": "user"
            },
            {
                "email": "usuario2@test.com", 
                "password": "password123",
                "nombre": "Usuario Prueba 2",
                "rol": "user"
            }
        ]
        
        for user_data in test_users:
            existing_user = db.query(models.Usuario).filter(
                models.Usuario.email == user_data["email"]
            ).first()
            
            if not existing_user:
                test_user = models.Usuario(
                    email=user_data["email"],
                    password=get_password_hash(user_data["password"]),
                    nombre=user_data["nombre"],
                    rol=user_data["rol"]
                )
                db.add(test_user)
                print(f"✅ Usuario {user_data['email']} creado")
        
        db.commit()
        db.close()
        
        print("\n🎉 ¡Base de datos inicializada correctamente!")
        print("\n🔑 Credenciales para probar:")
        print("   👨‍💼 Admin: admin@system.com / admin123")
        print("   👤 Usuario: usuario1@test.com / password123")
        print("   👤 Usuario: usuario2@test.com / password123")
        
    except Exception as e:
        print(f"❌ Error inicializando la base de datos: {e}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verificar que MySQL esté corriendo")
        print("   2. Crear la base de datos 'sistema_python' manualmente")
        print("   3. Verificar credenciales de MySQL en database.py")
        return False
    
    return True

def create_mysql_database():
    """Crea la base de datos en MySQL si no existe."""
    try:
        print("🗄️  Creando base de datos MySQL...")
        
        # Conectar a MySQL sin especificar base de datos
        mysql_url = "mysql+mysqlconnector://root@localhost/"
        temp_engine = create_engine(mysql_url)
        
        with temp_engine.connect() as conn:
            # Crear base de datos si no existe
            conn.execute(text("CREATE DATABASE IF NOT EXISTS sistema_python"))
            conn.commit()
        
        print("✅ Base de datos 'sistema_python' creada/verificada")
        return True
        
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        print("\n💡 Soluciones:")
        print("   1. Verificar que MySQL esté corriendo")
        print("   2. Verificar credenciales de root en MySQL")
        print("   3. Ejecutar MySQL como administrador")
        return False

if __name__ == "__main__":
    print("🚀 Inicializando Sistema de Agenda")
    print("=" * 40)
    
    # Crear base de datos
    if not create_mysql_database():
        sys.exit(1)
    
    # Inicializar tablas y datos
    if not init_database():
        sys.exit(1)
    
    print("\n✅ ¡Todo listo! Ahora puedes ejecutar:")
    print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")