-- INSERT para tabla parametro_hijo con parametro_id = 7 (Diagnósticos)
-- Estructura básica del INSERT

INSERT INTO parametro_hijo (
    parametro_id,
    nombre,
    descripcion,
    valor,
    estado,
    fecha_creacion
) VALUES (
    7,                    -- parametro_id = 7 (Diagnósticos)
    'NOMBRE_DIAGNOSTICO', -- Reemplazar con el nombre específico
    'DESCRIPCION_DIAGNOSTICO', -- Reemplazar con la descripción específica
    'VALOR_DIAGNOSTICO',  -- Reemplazar con el valor específico (opcional)
    1,                    -- estado = 1 (activo)
    NOW()                 -- fecha_creacion = fecha actual
);

-- Ejemplo con datos específicos (reemplazar con tus datos reales):
INSERT INTO parametro_hijo (
    parametro_id,
    nombre,
    descripcion,
    valor,
    estado,
    fecha_creacion
) VALUES 
    (7, 'Gripe', 'Infección viral del sistema respiratorio', 'GRIPE', 1, NOW()),
    (7, 'Migraña', 'Dolor de cabeza intenso y recurrente', 'MIGRAÑA', 1, NOW()),
    (7, 'Fractura', 'Ruptura o fisura en un hueso', 'FRACTURA', 1, NOW()),
    (7, 'Hipertensión', 'Presión arterial elevada', 'HIPERTENSION', 1, NOW()),
    (7, 'Diabetes', 'Alteración del metabolismo de la glucosa', 'DIABETES', 1, NOW());

-- Para insertar múltiples diagnósticos de una vez:
INSERT INTO parametro_hijo (parametro_id, nombre, descripcion, valor, estado, fecha_creacion) VALUES
    (7, 'Diagnóstico 1', 'Descripción del diagnóstico 1', 'VALOR1', 1, NOW()),
    (7, 'Diagnóstico 2', 'Descripción del diagnóstico 2', 'VALOR2', 1, NOW()),
    (7, 'Diagnóstico 3', 'Descripción del diagnóstico 3', 'VALOR3', 1, NOW());
    -- Agregar más filas según necesites

-- Verificar que se insertaron correctamente:
SELECT * FROM parametro_hijo WHERE parametro_id = 7 ORDER BY id_parametrohijo DESC;







