#!/usr/bin/env python3
"""
Script para configurar la base de datos MySQL
Ejecuta este script para crear las tablas automáticamente
"""

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import sys
from database import DATABASE_URL, Base
import models
from auth import get_password_hash

def create_database():
    """Crear la base de datos si no existe"""
    try:
        # Conectar sin especificar la base de datos
        base_url = DATABASE_URL.split('/')[:-1]
        base_url = '/'.join(base_url)
        engine = create_engine(base_url)
        
        with engine.connect() as conn:
            conn.execute(text("CREATE DATABASE IF NOT EXISTS sistema_python"))
            print("✅ Base de datos 'sistema_python' creada/verificada")
        
        engine.dispose()
        return True
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def create_tables():
    """Crear las tablas usando SQLAlchemy"""
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas correctamente")
        
        # Crear usuario admin por defecto
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            # Verificar si ya existe el admin
            admin_exists = db.query(models.Usuario).filter(
                models.Usuario.email == "admin@system.com"
            ).first()
            
            if not admin_exists:
                admin_user = models.Usuario(
                    email="admin@system.com",
                    password=get_password_hash("admin123"),
                    nombre="Administrador",
                    rol="admin"
                )
                db.add(admin_user)
                db.commit()
                print("✅ Usuario admin creado: admin@system.com / admin123")
            else:
                print("✅ Usuario admin ya existe")
                
        except Exception as e:
            print(f"❌ Error creando usuario admin: {e}")
            db.rollback()
        finally:
            db.close()
            
        engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return False

def verify_connection():
    """Verificar la conexión a MySQL"""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión a MySQL exitosa")
        engine.dispose()
        return True
    except OperationalError as e:
        print(f"❌ Error de conexión a MySQL: {e}")
        print("💡 Verifica que MySQL esté corriendo y las credenciales sean correctas")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    print("🚀 Configurando base de datos...")
    print(f"📍 URL de conexión: {DATABASE_URL}")
    
    # Paso 1: Verificar conexión
    if not verify_connection():
        print("\n❌ No se puede conectar a MySQL. Verifica:")
        print("1. MySQL está corriendo")
        print("2. Las credenciales en database.py son correctas")
        print("3. El usuario tiene permisos para crear bases de datos")
        sys.exit(1)
    
    # Paso 2: Crear base de datos
    if not create_database():
        sys.exit(1)
    
    # Paso 3: Crear tablas
    if not create_tables():
        sys.exit(1)
    
    print("\n🎉 ¡Base de datos configurada exitosamente!")
    print("📝 Credenciales de admin:")
    print("   Email: admin@system.com")
    print("   Password: admin123")
    print("\n🚀 Ahora puedes ejecutar: uvicorn main:app --reload")

if __name__ == "__main__":
    main()