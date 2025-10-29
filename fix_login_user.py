import sqlite3
from passlib.context import CryptContext

DB_PATH = r"C:/Users/Sistemas/Desktop/Incapacidades/incapacidades-backend-main/nueva_incapa.db"
EMAIL = "talentohumano@umit.com.co"
NEW_PASSWORD = "luz123"
NEW_ROLE = 10


def main() -> None:
    pwd = CryptContext(schemes=["bcrypt_sha256", "bcrypt"], deprecated="auto")
    hash_bcrypt = pwd.hash(NEW_PASSWORD)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id_usuario, correo_electronico FROM usuario
        WHERE lower(trim(correo_electronico)) = lower(trim(?))
        LIMIT 1
        """,
        (EMAIL,),
    )
    row = cur.fetchone()
    if not row:
        cur.execute("SELECT id_usuario, correo_electronico FROM usuario")
        rows = cur.fetchall()
        print("No se encontró el email. Correos existentes:")
        for r in rows:
            print("-", r[1])
        conn.close()
        raise SystemExit(1)

    user_id = row[0]
    print(f"Actualizando usuario id={user_id} email={row[1]!r}")

    cur.execute(
        """
        UPDATE usuario
        SET password = ?, estado = 1, rol_id = ?
        WHERE id_usuario = ?
        """,
        (hash_bcrypt, NEW_ROLE, user_id),
    )
    conn.commit()
    conn.close()
    print("OK: password (bcrypt), estado=1, rol_id=10")


if __name__ == "__main__":
    main()


