#!/usr/bin/env python3
"""
Script para verificar y ejecutar la inserción de diagnósticos en parametro_hijo
"""

import sqlite3
import os
from pathlib import Path

def verificar_y_ejecutar_diagnosticos():
    """Verifica la base de datos y ejecuta la inserción de diagnósticos"""
    
    # Ruta a la base de datos
    db_path = "incapacidades.db"
    sql_path = "insert_diagnosticos_completo.sql"
    
    print("🏥 Verificador y Ejecutor de Diagnósticos")
    print("=" * 50)
    
    # Verificar que existan los archivos
    if not os.path.exists(db_path):
        print(f"❌ Error: No se encontró la base de datos {db_path}")
        return False
    
    if not os.path.exists(sql_path):
        print(f"❌ Error: No se encontró el archivo SQL {sql_path}")
        return False
    
    print(f"✅ Base de datos encontrada: {db_path}")
    print(f"✅ Archivo SQL encontrado: {sql_path}")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estado actual
        print("\n📊 Estado actual de la base de datos:")
        cursor.execute("SELECT COUNT(*) FROM parametro_hijo WHERE parametro_id = 7")
        count_actual = cursor.fetchone()[0]
        print(f"   Diagnósticos existentes: {count_actual}")
        
        # Verificar estructura de la tabla
        cursor.execute("PRAGMA table_info(parametro_hijo)")
        columns = cursor.fetchall()
        print(f"   Columnas en parametro_hijo: {len(columns)}")
        for col in columns:
            print(f"     - {col[1]} ({col[2]})")
        
        # Preguntar si ejecutar la inserción
        if count_actual > 0:
            print(f"\n⚠️  Ya existen {count_actual} diagnósticos en la base de datos.")
            respuesta = input("¿Desea continuar y agregar más diagnósticos? (s/n): ").lower()
            if respuesta != 's':
                print("❌ Operación cancelada por el usuario")
                return False
        
        # Leer y ejecutar el archivo SQL
        print(f"\n📝 Ejecutando archivo SQL: {sql_path}")
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Ejecutar el SQL completo directamente
        print(f"   Ejecutando SQL completo...")
        
        try:
            cursor.executescript(sql_content)
            comandos_ejecutados = 1
            print(f"   ✅ SQL ejecutado exitosamente")
        except sqlite3.Error as e:
            print(f"❌ Error al ejecutar SQL: {e}")
            # Intentar ejecutar línea por línea como alternativa
            print("   🔄 Intentando ejecutar línea por línea...")
            lines = sql_content.split('\n')
            comandos_ejecutados = 0
            current_command = ""
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('--'):
                    current_command += line + " "
                    if line.endswith(';'):
                        try:
                            cursor.execute(current_command.strip())
                            comandos_ejecutados += 1
                            if comandos_ejecutados % 10 == 0:
                                print(f"   Procesados {comandos_ejecutados} comandos...")
                        except sqlite3.Error as e:
                            print(f"❌ Error en comando: {e}")
                            print(f"   Comando: {current_command[:100]}...")
                        current_command = ""
        
        # Confirmar cambios
        conn.commit()
        
        # Verificar resultado final
        cursor.execute("SELECT COUNT(*) FROM parametro_hijo WHERE parametro_id = 7")
        count_final = cursor.fetchone()[0]
        
        print(f"\n✅ Operación completada exitosamente!")
        print(f"📊 Diagnósticos antes: {count_actual}")
        print(f"📊 Diagnósticos después: {count_final}")
        print(f"📊 Diagnósticos agregados: {count_final - count_actual}")
        print(f"🔧 Comandos ejecutados: {comandos_ejecutados}")
        
        # Mostrar algunos ejemplos
        print(f"\n📋 Ejemplos de diagnósticos insertados:")
        cursor.execute("""
            SELECT nombre, descripcion 
            FROM parametro_hijo 
            WHERE parametro_id = 7 
            ORDER BY id_parametrohijo DESC 
            LIMIT 5
        """)
        
        ejemplos = cursor.fetchall()
        for i, (codigo, descripcion) in enumerate(ejemplos, 1):
            print(f"   {i}. {codigo} - {descripcion[:50]}{'...' if len(descripcion) > 50 else ''}")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Error de base de datos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = verificar_y_ejecutar_diagnosticos()
    if success:
        print("\n🎉 ¡Proceso completado exitosamente!")
    else:
        print("\n💥 El proceso falló. Revise los errores anteriores.")
