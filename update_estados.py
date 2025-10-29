#!/usr/bin/env python3
"""
Script para cambiar masivamente el estado de incapacidades.
Uso:
  python update_estados.py 1 12
"""

import sys
from typing import Optional

from app.db.session import get_db
from app.repositories.incapacidad import IncapacidadRepository


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("Uso: python update_estados.py <from_estado> <to_estado>")
        return 1

    try:
        from_estado = int(argv[1])
        to_estado = int(argv[2])
    except ValueError:
        print("Los estados deben ser números enteros")
        return 1

    db = next(get_db())
    repo = IncapacidadRepository(db)

    print(f"Cambiando estado de {from_estado} -> {to_estado}...")
    updated = repo.bulk_update_estado(from_estado=from_estado, to_estado=to_estado)
    print(f"Filas afectadas: {updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))


