#!/usr/bin/env python3
"""
Script para obtener los IDs reales de los parámetros (EPS, diagnóstico, servicio, causa)
"""

import sys
import os
from dotenv import load_dotenv

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import get_db
from app.repositories.parametro_hijo_repository import ParametroHijoRepository

def get_real_parameter_ids():
    """Obtiene los IDs reales de los parámetros"""
    print("🔍 Obteniendo IDs reales de parámetros")
    print("=" * 60)
    
    # Cargar configuración
    load_dotenv()
    
    try:
        db = next(get_db())
        param_repo = ParametroHijoRepository(db)
        
        # Obtener todos los parámetros
        print("📋 Obteniendo todos los parámetros...")
        all_params = param_repo.list()
        
        print(f"✅ Total de parámetros encontrados: {len(all_params)}")
        
        # Agrupar por tipo de parámetro
        eps_params = []
        diagnostico_params = []
        servicio_params = []
        causa_params = []
        
        for param in all_params:
            param_id = param.id_parametrohijo
            nombre = param.nombre or param.descripcion or "Sin nombre"
            padre_id = param.parametro_id
            
            # Determinar el tipo basado en el padre_id o nombre
            if "eps" in nombre.lower() or padre_id == 1:  # Asumiendo que EPS tiene padre_id = 1
                eps_params.append((param_id, nombre))
            elif "diagnostico" in nombre.lower() or "diagnóstico" in nombre.lower() or padre_id == 2:
                diagnostico_params.append((param_id, nombre))
            elif "servicio" in nombre.lower() or padre_id == 3:
                servicio_params.append((param_id, nombre))
            elif "causa" in nombre.lower() or "incapacidad" in nombre.lower() or padre_id == 4:
                causa_params.append((param_id, nombre))
        
        # Mostrar resultados
        print(f"\n🏥 PARÁMETROS EPS:")
        for param_id, nombre in eps_params[:10]:  # Mostrar solo los primeros 10
            print(f"   ID: {param_id} - {nombre}")
        if len(eps_params) > 10:
            print(f"   ... y {len(eps_params) - 10} más")
        
        print(f"\n🔬 PARÁMETROS DIAGNÓSTICO:")
        for param_id, nombre in diagnostico_params[:10]:
            print(f"   ID: {param_id} - {nombre}")
        if len(diagnostico_params) > 10:
            print(f"   ... y {len(diagnostico_params) - 10} más")
        
        print(f"\n🏢 PARÁMETROS SERVICIO:")
        for param_id, nombre in servicio_params[:10]:
            print(f"   ID: {param_id} - {nombre}")
        if len(servicio_params) > 10:
            print(f"   ... y {len(servicio_params) - 10} más")
        
        print(f"\n📋 PARÁMETROS CAUSA:")
        for param_id, nombre in causa_params[:10]:
            print(f"   ID: {param_id} - {nombre}")
        if len(causa_params) > 10:
            print(f"   ... y {len(causa_params) - 10} más")
        
        # Sugerir IDs para usar en pruebas
        print(f"\n💡 SUGERENCIAS PARA PRUEBAS:")
        if eps_params:
            print(f"   eps_afiliado_id: {eps_params[0][0]}  # {eps_params[0][1]}")
        if diagnostico_params:
            print(f"   diagnostico_id: {diagnostico_params[0][0]}  # {diagnostico_params[0][1]}")
        if servicio_params:
            print(f"   servicio_id: {servicio_params[0][0]}  # {servicio_params[0][1]}")
        if causa_params:
            print(f"   causa_id: {causa_params[0][0]}  # {causa_params[0][1]}")
        
        return {
            'eps': eps_params,
            'diagnostico': diagnostico_params,
            'servicio': servicio_params,
            'causa': causa_params
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo parámetros: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        if 'db' in locals():
            db.close()

def test_with_real_ids():
    """Prueba crear una incapacidad con IDs reales"""
    print(f"\n🧪 Probando con IDs reales...")
    
    # Obtener parámetros
    params = get_real_parameter_ids()
    if not params:
        return False
    
    # Usar los primeros IDs disponibles
    eps_id = params['eps'][0][0] if params['eps'] else 1
    diagnostico_id = params['diagnostico'][0][0] if params['diagnostico'] else 1
    servicio_id = params['servicio'][0][0] if params['servicio'] else 1
    causa_id = params['causa'][0][0] if params['causa'] else 1
    
    print(f"📝 IDs a usar:")
    print(f"   eps_afiliado_id: {eps_id}")
    print(f"   diagnostico_id: {diagnostico_id}")
    print(f"   servicio_id: {servicio_id}")
    print(f"   causa_id: {causa_id}")
    
    return True

if __name__ == "__main__":
    print("🔍 Obteniendo IDs Reales de Parámetros")
    print("=" * 60)
    
    success = get_real_parameter_ids()
    
    if success:
        test_with_real_ids()
    
    print(f"\n" + "=" * 60)
    print(f"🎉 ¡Proceso completado!")
    print(f"💡 Usa los IDs sugeridos en lugar de usar siempre '1'")
