#!/usr/bin/env python3
"""
Script para generar comandos INSERT MySQL para la tabla parametro_hijo
basado en el archivo diagnosticos.txt

Estructura de la tabla parametro_hijo:
- id_parametrohijo (AUTO_INCREMENT)
- parametro_id (INTEGER) - sera 7 para diagnosticos
- nombre (VARCHAR) - codigo del diagnostico (primera columna)
- descripcion (TEXT) - descripcion del diagnostico (segunda columna)
- estado (BOOLEAN) - sera 1 (activo)
"""

import os
import sys
from pathlib import Path

def procesar_diagnosticos_mysql():
    """Procesa el archivo de diagnosticos y genera SQL MySQL para parametro_hijo"""
    
    # Ruta al archivo de diagnosticos
    archivo_diagnosticos = Path("../incapacidades froend/incapacidades/public/diagnosticos.txt")
    
    if not archivo_diagnosticos.exists():
        print(f"Error: No se encontro el archivo {archivo_diagnosticos}")
        return
    
    print(f"Procesando archivo: {archivo_diagnosticos}")
    
    # Leer el archivo
    try:
        with open(archivo_diagnosticos, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return
    
    # Procesar lineas y extraer diagnosticos
    diagnosticos = []
    for i, linea in enumerate(lineas):
        linea = linea.strip()
        
        # Saltar lineas vacias o de encabezado
        if not linea or linea.startswith("COD_4") or linea.startswith("DESCRIPCION"):
            continue
        
        # Buscar patron: CODIGO + DESCRIPCION (separados por tab)
        partes = linea.split('\t', 1)  # Dividir por tab
        if len(partes) >= 2:
            codigo = partes[0].strip()
            descripcion = partes[1].strip()
            
            # Validar que el codigo tenga formato valido (ej: A000, B123, etc.)
            if len(codigo) >= 4 and codigo[0].isalpha() and codigo[1:].isdigit():
                diagnosticos.append({
                    'codigo': codigo,
                    'descripcion': descripcion
                })
    
    print(f"Se encontraron {len(diagnosticos)} diagnosticos validos")
    
    # Generar archivo SQL MySQL
    generar_sql_mysql(diagnosticos)
    
    return diagnosticos

def generar_sql_mysql(diagnosticos):
    """Genera archivo SQL MySQL con los INSERT para parametro_hijo"""
    
    archivo_sql = "insert_diagnosticos_mysql.sql"
    
    print(f"Generando archivo SQL MySQL: {archivo_sql}")
    
    with open(archivo_sql, 'w', encoding='utf-8') as f:
        f.write("-- =====================================================\n")
        f.write("-- INSERT para tabla parametro_hijo con parametro_id = 7 (Diagnosticos)\n")
        f.write("-- Generado automaticamente desde diagnosticos.txt\n")
        f.write("-- Base de datos: MySQL\n")
        f.write("-- Total de diagnosticos: {}\n".format(len(diagnosticos)))
        f.write("-- =====================================================\n\n")
        
        # Configuracion inicial para MySQL
        f.write("-- Configuracion inicial para MySQL\n")
        f.write("SET NAMES utf8mb4;\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
        
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
                # Escapar comillas simples y caracteres especiales para MySQL
                descripcion_escaped = diag['descripcion'].replace("'", "\\'").replace('"', '\\"')
                nombre_escaped = diag['codigo'].replace("'", "\\'").replace('"', '\\"')
                
                valor = f"(7, '{nombre_escaped}', '{descripcion_escaped}', 1)"
                valores.append(valor)
            
            f.write(",\n".join(valores))
            f.write(";\n\n")
        
        # Restaurar configuracion
        f.write("-- Restaurar configuracion\n")
        f.write("SET FOREIGN_KEY_CHECKS = 1;\n\n")
        
        # Agregar consultas de verificacion
        f.write("-- =====================================================\n")
        f.write("-- CONSULTAS DE VERIFICACION\n")
        f.write("-- =====================================================\n\n")
        f.write("-- Verificar total de diagnosticos insertados:\n")
        f.write("SELECT COUNT(*) as total_diagnosticos FROM parametro_hijo WHERE parametro_id = 7;\n\n")
        f.write("-- Mostrar algunos ejemplos:\n")
        f.write("SELECT id_parametrohijo, nombre, descripcion, estado \n")
        f.write("FROM parametro_hijo \n")
        f.write("WHERE parametro_id = 7 \n")
        f.write("ORDER BY id_parametrohijo DESC \n")
        f.write("LIMIT 10;\n\n")
        f.write("-- Buscar un diagnostico especifico (ejemplo):\n")
        f.write("-- SELECT * FROM parametro_hijo WHERE parametro_id = 7 AND nombre LIKE 'A000%';\n\n")
        f.write("-- Verificar estructura de la tabla:\n")
        f.write("-- DESCRIBE parametro_hijo;\n")
    
    print(f"Archivo SQL MySQL generado: {archivo_sql}")
    print(f"Total de diagnosticos procesados: {len(diagnosticos)}")

def mostrar_ejemplos(diagnosticos, cantidad=10):
    """Muestra ejemplos de los diagnosticos encontrados"""
    print(f"\nEjemplos de diagnosticos encontrados (primeros {cantidad}):")
    print("-" * 80)
    
    for i, diag in enumerate(diagnosticos[:cantidad]):
        print(f"{i+1:3d}. {diag['codigo']} - {diag['descripcion'][:60]}{'...' if len(diag['descripcion']) > 60 else ''}")
    
    if len(diagnosticos) > cantidad:
        print(f"... y {len(diagnosticos) - cantidad} mas")

if __name__ == "__main__":
    print("Generador de INSERT MySQL para Diagnosticos")
    print("=" * 60)
    
    diagnosticos = procesar_diagnosticos_mysql()
    
    if diagnosticos:
        mostrar_ejemplos(diagnosticos)
        
        print(f"\nProceso completado exitosamente!")
        print(f"Archivo SQL MySQL generado: insert_diagnosticos_mysql.sql")
        print(f"Para ejecutar en MySQL:")
        print(f"   mysql -u usuario -p base_datos < insert_diagnosticos_mysql.sql")
        print(f"\nResumen:")
        print(f"   - Total diagnosticos: {len(diagnosticos)}")
        print(f"   - parametro_id: 7")
        print(f"   - estado: 1 (activo)")
        print(f"   - id_parametrohijo: AUTO_INCREMENT")
    else:
        print("No se pudieron procesar los diagnosticos")

