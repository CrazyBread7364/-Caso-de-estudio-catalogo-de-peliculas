#!/usr/bin/env python3
"""
Script de automatización para la creación y restauración de la base de datos PostgreSQL 'caescapel'.
Compatible con Windows, macOS y Linux.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Configurar encoding UTF-8 en stdout si es posible
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent
BACKUP_FILE = BASE_DIR / "backup_completo_caescapel.sql"

# Parámetros de conexión
DB_NAME = os.getenv("DB_NAME", "caescapel")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")


def find_psql() -> str:
    """Localiza el ejecutable psql en el PATH o en rutas comunes del sistema."""
    path_psql = shutil.which("psql")
    if path_psql:
        return path_psql

    if sys.platform.startswith("win"):
        common_dirs = [
            Path("C:/Program Files/PostgreSQL"),
            Path("C:/Program Files (x86)/PostgreSQL"),
        ]
        for cdir in common_dirs:
            if cdir.exists():
                candidates = sorted(cdir.glob("*/bin/psql.exe"), reverse=True)
                if candidates:
                    return str(candidates[0])

    print("[ERROR] No se encontró el ejecutable 'psql'.", file=sys.stderr)
    print("Asegúrate de que PostgreSQL esté instalado o agrega su carpeta bin al PATH.", file=sys.stderr)
    sys.exit(1)


def run_command(cmd: list[str], env: dict[str, str], check: bool = True) -> subprocess.CompletedProcess:
    """Ejecuta un comando con variables de entorno personalizadas."""
    return subprocess.run(
        cmd,
        env=env,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def main():
    print("=" * 60)
    print("  Inicializador y Restaurador de Base de Datos PostgreSQL")
    print("=" * 60)

    psql = find_psql()
    print(f"[+] Usando psql: {psql}")

    if not BACKUP_FILE.exists():
        print(f"[ERROR] No se encontró el archivo de respaldo: {BACKUP_FILE}", file=sys.stderr)
        sys.exit(1)
    print(f"[+] Archivo de respaldo: {BACKUP_FILE}")

    env = os.environ.copy()
    env["PGPASSWORD"] = DB_PASSWORD

    # 1. Comprobar si la base de datos existe
    print(f"\n[1/3] Verificando existencia de la base de datos '{DB_NAME}'...")
    check_cmd = [
        psql,
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-U", DB_USER,
        "-d", "postgres",
        "-tAc", f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}';",
    ]
    res_check = run_command(check_cmd, env, check=False)
    db_exists = res_check.stdout.strip() == "1"

    if db_exists:
        print(f"[OK] La base de datos '{DB_NAME}' ya existe.")
    else:
        print(f"[+] Creando base de datos '{DB_NAME}'...")
        create_cmd = [
            psql,
            "-h", DB_HOST,
            "-p", DB_PORT,
            "-U", DB_USER,
            "-d", "postgres",
            "-c", f"CREATE DATABASE {DB_NAME};",
        ]
        res_create = run_command(create_cmd, env, check=False)
        if res_create.returncode != 0:
            print(f"[ERROR] Falló la creación de la base de datos:\n{res_create.stderr}", file=sys.stderr)
            sys.exit(res_create.returncode)
        print(f"[OK] Base de datos '{DB_NAME}' creada exitosamente.")

    # 2. Restaurar backup SQL
    print(f"\n[2/3] Restaurando tablas y datos desde '{BACKUP_FILE.name}'...")
    restore_cmd = [
        psql,
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-U", DB_USER,
        "-d", DB_NAME,
        "-f", str(BACKUP_FILE),
    ]
    res_restore = run_command(restore_cmd, env, check=False)
    if res_restore.returncode != 0:
        print(f"[ALERTA] psql finalizó con código {res_restore.returncode}:\n{res_restore.stderr}")
    else:
        print("[OK] Restauración completada exitosamente.")

    # 3. Validar películas cargadas
    print(f"\n[3/3] Validando datos en 'MovieService_movie'...")
    validate_cmd = [
        psql,
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-U", DB_USER,
        "-d", DB_NAME,
        "-tAc", 'SELECT count(*) FROM "MovieService_movie";',
    ]
    res_validate = run_command(validate_cmd, env, check=False)
    count = res_validate.stdout.strip()
    if count.isdigit():
        print(f"[ÉXITO] {count} películas registradas y verificadas en la base de datos.")
    else:
        print("[INFO] No se pudo obtener el conteo exacto de películas.")

    print("\n" + "=" * 60)
    print("  ¡Base de datos lista para usarse con Django!")
    print("=" * 60)


if __name__ == "__main__":
    main()
