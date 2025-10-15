#!/usr/bin/env python3
"""
Script para verificar el esquema de la base de datos.
"""
from sqlalchemy import create_engine, text, inspect
from database import DATABASE_URL
import pandas as pd

def check_database_schema():
    """Verifica y muestra el esquema de la base de datos."""
    try:
        engine = create_engine(DATABASE_URL)
        inspector = inspect(engine)
        
        print("🗄️  ESQUEMA DE LA BASE DE DATOS")
        print("=" * 50)
        
        # Obtener lista de tablas
        tables = inspector.get_table_names()
        print(f"📊 Tablas encontradas: {len(tables)}")
        print(f"   {', '.join(tables)}")
        print()
        
        # Mostrar estructura de cada tabla
        with engine.connect() as conn:
            for table_name in tables:
                print(f"📋 Tabla: {table_name.upper()}")
                print("-" * 30)
                
                # Obtener columnas
                columns = inspector.get_columns(table_name)
                print("Columnas:")
                for col in columns:
                    nullable = "NULL" if col['nullable'] else "NOT NULL"
                    default = f" DEFAULT {col['default']}" if col['default'] is not None else ""
                    print(f"  • {col['name']}: {col['type']} {nullable}{default}")
                
                # Obtener llaves primarias
                pk_constraint = inspector.get_pk_constraint(table_name)
                if pk_constraint['constrained_columns']:
                    print(f"🔑 Primary Key: {', '.join(pk_constraint['constrained_columns'])}")
                
                # Obtener llaves foráneas
                fk_constraints = inspector.get_foreign_keys(table_name)
                if fk_constraints:
                    print("🔗 Foreign Keys:")
                    for fk in fk_constraints:
                        print(f"  • {fk['constrained_columns'][0]} -> {fk['referred_table']}.{fk['referred_columns'][0]}")
                
                # Mostrar datos de la tabla
                result = conn.execute(text(f"SELECT COUNT(*) as total FROM {table_name}"))
                count = result.fetchone()[0]
                print(f"📊 Total de registros: {count}")
                
                if count > 0 and count <= 10:
                    print("🔍 Datos de muestra:")
                    result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 5"))
                    rows = result.fetchall()
                    columns_names = result.keys()
                    
                    # Mostrar como tabla
                    if rows:
                        df = pd.DataFrame(rows, columns=columns_names)
                        print(df.to_string(index=False))
                
                print("\n" + "="*50 + "\n")
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")

def show_users_with_passwords():
    """Muestra todos los usuarios con información sobre sus passwords."""
    try:
        engine = create_engine(DATABASE_URL)
        
        print("👥 USUARIOS EN EL SISTEMA")
        print("=" * 50)
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    id,
                    email,
                    nombre,
                    rol,
                    LEFT(password, 20) as password_hash,
                    fecha_creacion
                FROM usuarios 
                ORDER BY id
            """))
            
            rows = result.fetchall()
            columns_names = result.keys()
            
            if rows:
                df = pd.DataFrame(rows, columns=columns_names)
                print(df.to_string(index=False))
                
                print("\n🔑 CREDENCIALES DE PRUEBA:")
                print("👨‍💼 Admin: admin@system.com / admin123")
                print("👤 Usuario 1: usuario1@test.com / password123") 
                print("👤 Usuario 2: usuario2@test.com / password123")
            else:
                print("⚠️  No se encontraron usuarios")
                
    except Exception as e:
        print(f"❌ Error obteniendo usuarios: {e}")

if __name__ == "__main__":
    check_database_schema()
    print("\n")
    show_users_with_passwords()