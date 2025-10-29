#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar INSERT de cargos en la tabla parametro_hijo
parametro_id = 4 (Cargos)
"""

import os
import re

def procesar_cargos():
    """Procesa el archivo cargos.txt y genera INSERT statements"""
    
    # Ruta del archivo cargos.txt
    archivo_cargos = "../incapacidades froend/incapacidades/public/cargos.txt"
    
    if not os.path.exists(archivo_cargos):
        print(f"Error: No se encontro el archivo {archivo_cargos}")
        return 0, 0
    
    try:
        with open(archivo_cargos, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        # Filtrar líneas vacías y procesar
        cargos = []
        for linea in lineas:
            linea = linea.strip()
            if linea and linea != '':
                # Dividir por tabulaciones múltiples
                partes = re.split(r'\t+', linea)
                if len(partes) >= 2:
                    nombre = partes[0].strip()
                    descripcion = partes[1].strip()
                    
                    # Limpiar nombres y descripciones
                    nombre = nombre.replace('"', '\\"').replace("'", "\\'")
                    descripcion = descripcion.replace('"', '\\"').replace("'", "\\'")
                    
                    if nombre and descripcion:
                        cargos.append((nombre, descripcion))
        
        print(f"Cargos encontrados: {len(cargos)}")
        
        # Generar SQL
        sql_content = generar_sql_cargos(cargos)
        
        # Guardar archivo SQL
        archivo_sql = "insert_cargos_mysql.sql"
        with open(archivo_sql, 'w', encoding='utf-8') as f:
            f.write(sql_content)
        
        print(f"Archivo SQL generado: {archivo_sql}")
        print(f"Total de cargos procesados: {len(cargos)}")
        
        return len(cargos), len(cargos)
        
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return 0, 0

def generar_sql_cargos(cargos):
    """Genera el contenido SQL para los cargos"""
    
    sql_lines = [
        "-- =====================================================",
        "-- INSERT para tabla parametro_hijo con parametro_id = 4 (Cargos)",
        "-- Generado automaticamente desde cargos.txt",
        "-- Base de datos: MySQL",
        f"-- Total de cargos: {len(cargos)}",
        "-- =====================================================",
        "",
        "-- Configuracion inicial para MySQL",
        "SET NAMES utf8mb4;",
        "SET FOREIGN_KEY_CHECKS = 0;",
        "",
        "-- Limpiar datos existentes (opcional)",
        "-- DELETE FROM parametro_hijo WHERE parametro_id = 4;",
        "",
    ]
    
    # Procesar en lotes de 50
    lote_size = 50
    total_lotes = (len(cargos) + lote_size - 1) // lote_size
    
    for i in range(0, len(cargos), lote_size):
        lote_num = (i // lote_size) + 1
        lote_cargos = cargos[i:i + lote_size]
        
        sql_lines.append(f"-- Lote {lote_num} de {total_lotes} (registros {i+1}-{min(i+lote_size, len(cargos))})")
        sql_lines.append("INSERT INTO parametro_hijo (parametro_id, nombre, descripcion, estado) VALUES")
        
        valores = []
        for nombre, descripcion in lote_cargos:
            valor = f"(4, '{nombre}', '{descripcion}', 1)"
            valores.append(valor)
        
        sql_lines.append(",\n".join(valores) + ";")
        sql_lines.append("")
    
    sql_lines.extend([
        "-- Restaurar configuracion",
        "SET FOREIGN_KEY_CHECKS = 1;",
        "",
        "-- Verificar insercion",
        f"SELECT COUNT(*) as total_cargos FROM parametro_hijo WHERE parametro_id = 4;",
        "",
        "-- Mostrar algunos ejemplos",
        "SELECT id_parametrohijo, nombre, descripcion FROM parametro_hijo WHERE parametro_id = 4 LIMIT 10;"
    ])
    
    return "\n".join(sql_lines)

if __name__ == "__main__":
    print("Generando INSERT para cargos (parametro_id = 4)")
    print("=" * 50)
    
    total_procesados, total_generados = procesar_cargos()
    
    if total_procesados > 0:
        print(f"\nProceso completado exitosamente!")
        print(f"Cargos procesados: {total_procesados}")
        print(f"Archivo SQL generado: insert_cargos_mysql.sql")
        print(f"\nPara ejecutar en MySQL:")
        print(f"   mysql -u usuario -p base_datos < insert_cargos_mysql.sql")
    else:
        print(f"\nNo se pudieron procesar los cargos")
