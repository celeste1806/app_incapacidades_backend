#!/usr/bin/env python3

from app.db.session import SessionLocal
from app.repositories.usuario_repository import UsuarioRepository
from app.core.security import verify_password


def main() -> None:
    email = "talentohumano@umit.com.co"
    test_passwords = [
        "123456",
        "Password123",
        "Talento2024",
    ]

    with SessionLocal() as db:
        repo = UsuarioRepository(db)

        print("=== LISTA DE CORREOS EN TABLA usuario ===")
        try:
            users = repo.list(limit=200)
            for u in users:
                print(f"- {u.correo_electronico!r} (rol_id={u.rol_id}, estado={u.estado})")
        except Exception as e:
            print("[ERR] No se pudo listar usuarios:", e)

        print("\n=== BUSCANDO POR EMAIL NORMALIZADO ===")
        user = repo.get_by_email(email)
        if user is None:
            print(f"[NOT_FOUND] No existe usuario con email: {email}")
            return

        print(f"[FOUND] Usuario: id={user.id_usuario}, email={user.correo_electronico!r}, rol_id={user.rol_id}, estado={user.estado}")
        print(f"Hash (primeros 30): {user.password[:30]}...")

        for pw in test_passwords:
            try:
                ok = verify_password(pw, user.password)
            except Exception as e:
                ok = False
                print(f"verify_password error para '{pw}': {e}")
            print(f"verify_password('{pw}') => {ok}")


if __name__ == "__main__":
    main()


