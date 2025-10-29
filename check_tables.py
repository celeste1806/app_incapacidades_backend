#!/usr/bin/env python3
"""
Script para verificar las tablas de usuarios
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine
from sqlalchemy import inspect

def check_user_tables():
    """Verifica las tablas de usuarios"""
    print("🔍 Verificando tablas de usuarios...")
    
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"📋 Tablas existentes: {len(tables)}")
        for table in tables:
            print(f"  - {table}")
        
        # Verificar tabla 'usuario'
        if 'usuario' in tables:
            print(f"\n📊 Estructura de tabla 'usuario':")
            columns = inspector.get_columns('usuario')
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
        
        # Verificar tabla 'usuarios'
        if 'usuarios' in tables:
            print(f"\n📊 Estructura de tabla 'usuarios':")
            columns = inspector.get_columns('usuarios')
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    check_user_tables()

