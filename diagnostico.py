#!/usr/bin/env python3

print("=== DIAGNÓSTICO DEL PROYECTO ===")
print()

# Verificar Python
import sys
print(f"Python version: {sys.version}")
print()

# Verificar dependencias
dependencias = [
    'fastapi',
    'uvicorn', 
    'sqlalchemy',
    'pydantic',
    'python-multipart'
]

print("Verificando dependencias:")
for dep in dependencias:
    try:
        module = __import__(dep)
        version = getattr(module, '__version__', 'N/A')
        print(f"✓ {dep}: {version}")
    except ImportError:
        print(f"✗ {dep}: NO INSTALADO")

print()

# Verificar importaciones del proyecto
print("Verificando importaciones del proyecto:")
try:
    from app.api.main import app
    print("✓ app.api.main importado correctamente")
except Exception as e:
    print(f"✗ Error importando app.api.main: {e}")
    import traceback
    traceback.print_exc()

print()

# Verificar servicios
servicios = [
    'app.services.upload_service',
    'app.services.notification_service', 
    'app.services.audit_service',
    'app.services.incapacidad_service'
]

print("Verificando servicios:")
for servicio in servicios:
    try:
        __import__(servicio)
        print(f"✓ {servicio}")
    except Exception as e:
        print(f"✗ {servicio}: {e}")

print()

# Verificar routers
routers = [
    'app.api.v1.routers.upload_router',
    'app.api.v1.routers.incapacidad_router'
]

print("Verificando routers:")
for router in routers:
    try:
        __import__(router)
        print(f"✓ {router}")
    except Exception as e:
        print(f"✗ {router}: {e}")

print()
print("=== FIN DEL DIAGNÓSTICO ===")
