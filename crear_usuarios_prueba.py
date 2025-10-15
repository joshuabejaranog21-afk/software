"""
Script para crear los usuarios de prueba para el profesor
"""
from database import SessionLocal
from models import Usuario
from auth import get_password_hash

def crear_usuarios_prueba():
    db = SessionLocal()

    try:
        # Usuario 1: Usuario Normal
        usuario_normal = db.query(Usuario).filter(Usuario.email == "usuario_nuevo@test.com").first()
        if not usuario_normal:
            usuario_normal = Usuario(
                email="usuario_nuevo@test.com",
                password=get_password_hash("1234567"),
                nombre="Usuario Prueba",
                rol="user"
            )
            db.add(usuario_normal)
            print("✅ Usuario normal creado: usuario_nuevo@test.com")
        else:
            print("ℹ️  Usuario normal ya existe: usuario_nuevo@test.com")

        # Usuario 2: Administrador
        usuario_admin = db.query(Usuario).filter(Usuario.email == "bejaranojoshua@gmail.com").first()
        if not usuario_admin:
            usuario_admin = Usuario(
                email="bejaranojoshua@gmail.com",
                password=get_password_hash("123456"),
                nombre="Joshua Bejarano",
                rol="admin"
            )
            db.add(usuario_admin)
            print("✅ Usuario admin creado: bejaranojoshua@gmail.com")
        else:
            print("ℹ️  Usuario admin ya existe: bejaranojoshua@gmail.com")

        db.commit()
        print("\n✨ Usuarios de prueba listos!")
        print("\n📋 Credenciales disponibles:")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("👤 Usuario Normal:")
        print("   Email: usuario_nuevo@test.com")
        print("   Password: 1234567")
        print("\n👨‍💼 Administrador:")
        print("   Email: bejaranojoshua@gmail.com")
        print("   Password: 123456")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    crear_usuarios_prueba()
