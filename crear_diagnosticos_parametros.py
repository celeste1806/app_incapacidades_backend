#!/usr/bin/env python3
"""
Script para crear parámetros hijo de diagnósticos (parametro_id = 7) 
basado en el archivo diagnosticos.txt
"""

import os
import sys
from pathlib import Path

def procesar_diagnosticos():
    """Procesa el archivo de diagnósticos y genera SQL para parametro_hijo"""
    
    # Ruta al archivo de diagnósticos
    archivo_diagnosticos = Path("../incapacidades froend/incapacidades/public/diagnosticos.txt")
    
    if not archivo_diagnosticos.exists():
        print(f"❌ Error: No se encontró el archivo {archivo_diagnosticos}")
        return
    
    print(f"📖 Procesando archivo: {archivo_diagnosticos}")
    
    # Leer el archivo
    try:
        with open(archivo_diagnosticos, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return
    
    # Procesar líneas y extraer diagnósticos
    diagnosticos = []
    for i, linea in enumerate(lineas):
        linea = linea.strip()
        
        # Saltar líneas vacías o de encabezado
        if not linea or linea.startswith("COD_4") or linea.startswith("DESCRIPCION"):
            continue
        
        # Buscar patrón: CÓDIGO + DESCRIPCIÓN
        partes = linea.split('\t', 1)  # Dividir por tab
        if len(partes) >= 2:
            codigo = partes[0].strip()
            descripcion = partes[1].strip()
            
            # Validar que el código tenga formato válido (ej: A000, B123, etc.)
            if len(codigo) >= 4 and codigo[0].isalpha() and codigo[1:].isdigit():
                diagnosticos.append({
                    'codigo': codigo,
                    'descripcion': descripcion
                })
    
    print(f"✅ Se encontraron {len(diagnosticos)} diagnósticos válidos")
    
    # Generar archivo SQL
    generar_sql_diagnosticos(diagnosticos)
    
    return diagnosticos

def generar_sql_diagnosticos(diagnosticos):
    """Genera archivo SQL con los INSERT para parametro_hijo"""
    
    archivo_sql = "insert_diagnosticos_completo.sql"
    
    print(f"📝 Generando archivo SQL: {archivo_sql}")
    
    with open(archivo_sql, 'w', encoding='utf-8') as f:
        f.write("-- INSERT para tabla parametro_hijo con parametro_id = 7 (Diagnósticos)\n")
        f.write("-- Generado automáticamente desde diagnosticos.txt\n")
        f.write("-- Total de diagnósticos: {}\n\n".format(len(diagnosticos)))
        
        # Escribir INSERTs en lotes de 100 para mejor rendimiento
        batch_size = 100
        total_batches = (len(diagnosticos) + batch_size - 1) // batch_size
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(diagnosticos))
            batch_diagnosticos = diagnosticos[start_idx:end_idx]
            
            f.write(f"-- Lote {batch_num + 1} de {total_batches} (registros {start_idx + 1}-{end_idx})\n")
            f.write("INSERT INTO parametro_hijo (parametro_id, nombre, descripcion, estado) VALUES\n")
            
            valores = []
            for diag in batch_diagnosticos:
                # Escapar comillas simples en la descripción
                descripcion_escaped = diag['descripcion'].replace("'", "''")
                nombre_escaped = diag['codigo'].replace("'", "''")
                
                valor = f"(7, '{nombre_escaped}', '{descripcion_escaped}', 1)"
                valores.append(valor)
            
            f.write(",\n".join(valores))
            f.write(";\n\n")
        
        # Agregar consulta de verificación
        f.write("-- Verificar que se insertaron correctamente:\n")
        f.write("SELECT COUNT(*) as total_diagnosticos FROM parametro_hijo WHERE parametro_id = 7;\n\n")
        f.write("-- Mostrar algunos ejemplos:\n")
        f.write("SELECT * FROM parametro_hijo WHERE parametro_id = 7 ORDER BY id_parametrohijo DESC LIMIT 10;\n")
    
    print(f"✅ Archivo SQL generado: {archivo_sql}")
    print(f"📊 Total de diagnósticos procesados: {len(diagnosticos)}")

def mostrar_ejemplos(diagnosticos, cantidad=10):
    """Muestra ejemplos de los diagnósticos encontrados"""
    print(f"\n📋 Ejemplos de diagnósticos encontrados (primeros {cantidad}):")
    print("-" * 80)
    
    for i, diag in enumerate(diagnosticos[:cantidad]):
        print(f"{i+1:3d}. {diag['codigo']} - {diag['descripcion'][:60]}{'...' if len(diag['descripcion']) > 60 else ''}")
    
    if len(diagnosticos) > cantidad:
        print(f"... y {len(diagnosticos) - cantidad} más")

if __name__ == "__main__":
    print("🏥 Procesador de Diagnósticos para Parámetros Hijo")
    print("=" * 60)
    
    diagnosticos = procesar_diagnosticos()
    
    if diagnosticos:
        mostrar_ejemplos(diagnosticos)
        print(f"\n✅ Proceso completado exitosamente!")
        print(f"📁 Archivo SQL generado: insert_diagnosticos_completo.sql")
        print(f"🔧 Para ejecutar: sqlite3 incapacidades.db < insert_diagnosticos_completo.sql")
    else:
        print("❌ No se pudieron procesar los diagnósticos")
