#!/usr/bin/env python3
"""
Script para verificar usuarios en la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import get_db
from app.repositories.usuario_repository import UsuarioRepository

def check_users():
    db = next(get_db())
    repo = UsuarioRepository(db)
    
    print("=== USUARIOS EN LA BASE DE DATOS ===")
    
    # Obtener todos los usuarios
    usuarios = repo.list(limit=100)
    
    for usuario in usuarios:
        print(f"ID: {usuario.id_usuario}")
        print(f"  Email: {usuario.correo_electronico}")
        print(f"  Nombre: {usuario.nombre_completo}")
        print(f"  Rol: {usuario.rol_id}")
        print(f"  Estado: {usuario.estado}")
        print(f"  Password hash: {usuario.password[:20]}...")
        print()

if __name__ == "__main__":
    check_users()
