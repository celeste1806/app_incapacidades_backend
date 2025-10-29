from sqlalchemy import text
from sqlalchemy.engine import Engine


def column_exists(engine: Engine, table_name: str, column_name: str) -> bool:
    sql = text(
        """
        SELECT 1
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = :table
          AND COLUMN_NAME = :column
        LIMIT 1
        """
    )
    with engine.connect() as conn:
        return conn.execute(sql, {"table": table_name, "column": column_name}).first() is not None


def fk_exists(engine: Engine, table_name: str, constraint_name: str) -> bool:
    sql = text(
        """
        SELECT 1
        FROM information_schema.TABLE_CONSTRAINTS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = :table
          AND CONSTRAINT_NAME = :cname
          AND CONSTRAINT_TYPE = 'FOREIGN KEY'
        LIMIT 1
        """
    )
    with engine.connect() as conn:
        return conn.execute(sql, {"table": table_name, "cname": constraint_name}).first() is not None


def _is_mysql(engine: Engine) -> bool:
    # Detecta si el dialecto activo es MySQL/MariaDB
    name = getattr(engine.dialect, "name", "").lower()
    return name.startswith("mysql")


def align_usuario_table(engine: Engine) -> None:
    # Evitar ejecutar migraciones específicas de MySQL en otros motores (p.ej., SQLite)
    if not _is_mysql(engine):
        return
    # Detectar nombre real de la tabla (sensible a mayúsculas según FS/configuración)
    table = "Usuario"
    try:
        if column_exists(engine, "usuario", "id_usuario"):
            table = "usuario"
    except Exception:
        pass
    # 1) cargo_interno_id
    has_cargo_interno_id = column_exists(engine, table, "cargo_interno_id")
    has_cargo_interno = column_exists(engine, table, "cargo_interno")
    with engine.begin() as conn:
        if not has_cargo_interno_id and has_cargo_interno:
            conn.execute(text("ALTER TABLE `Usuario` CHANGE COLUMN `cargo_interno` `cargo_interno_id` INT NOT NULL"))
            has_cargo_interno_id = True
        if not has_cargo_interno_id and not has_cargo_interno:
            conn.execute(text("ALTER TABLE `Usuario` ADD COLUMN `cargo_interno_id` INT NOT NULL"))

        # 2) asegurar tipos INT en otras columnas
        for col in ("tipo_identificacion_id", "tipo_empleador_id", "rol_id"):
            if column_exists(engine, table, col):
                conn.execute(text(f"ALTER TABLE `{table}` MODIFY `{col}` INT"))

        # 3) crear FKs si no existen
        fks = {
            "fk_usuario_cargo_interno": "cargo_interno_id",
            "fk_usuario_tipo_identificacion": "tipo_identificacion_id",
            "fk_usuario_tipo_empleador": "tipo_empleador_id",
            "fk_usuario_rol": "rol_id",
        }
        for cname, col in fks.items():
            if column_exists(engine, table, col) and not fk_exists(engine, table, cname):
                conn.execute(
                    text(
                        f"""
                        ALTER TABLE `{table}`
                        ADD CONSTRAINT `{cname}`
                        FOREIGN KEY (`{col}`) REFERENCES `parametro_hijo`(`id_parametrohijo`)
                        """
                    )
                )

        # 4) agregar columna telefono si no existe
        if not column_exists(engine, table, "telefono"):
            conn.execute(text(f"ALTER TABLE `{table}` ADD COLUMN `telefono` VARCHAR(30) NULL"))



def align_incapacidad_table(engine: Engine) -> None:
    """Alinea la columna fecha_registro para que NO se actualice en cada UPDATE.
    - Aplica solo en MySQL/MariaDB
    - Quita la cláusula 'ON UPDATE CURRENT_TIMESTAMP' si existe
    - Establece DEFAULT CURRENT_TIMESTAMP únicamente en creación
    """
    if not _is_mysql(engine):
        return

    table = "incapacidad"
    if not column_exists(engine, table, "fecha_registro"):
        return

    # Detectar si la columna tiene ON UPDATE CURRENT_TIMESTAMP
    sql_inspect = text(
        """
        SELECT DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, EXTRA
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = :table
          AND COLUMN_NAME = 'fecha_registro'
        LIMIT 1
        """
    )
    with engine.begin() as conn:
        row = conn.execute(sql_inspect, {"table": table}).first()
        if not row:
            return
        data_type = (row[0] or "").lower()  # datetime o timestamp
        is_nullable = (row[1] or "NO").upper()  # 'YES'/'NO'
        extra = (row[3] or "").lower()

        # Si tiene 'on update', lo removemos re-declarando la columna sin esa cláusula
        if "on update" in extra:
            # Construir tipo base conservando NOT NULL y DEFAULT CURRENT_TIMESTAMP
            # Usar DATETIME para evitar autoupdate implícito de TIMESTAMP
            not_null = "NOT NULL" if is_nullable == "NO" else "NULL"
            # Forzamos DEFAULT CURRENT_TIMESTAMP para creación
            conn.execute(
                text(
                    f"ALTER TABLE `{table}` MODIFY `fecha_registro` DATETIME {not_null} DEFAULT CURRENT_TIMESTAMP"
                )
            )

