import sqlite
import hashlib

# Conectar a la base de datos
conn = sqlite.connect('nueva_incapa.db')
cursor = conn.cursor()

# Ver usuarios existentes
cursor.execute("SELECT id_usuario, nombre_completo FROM usuario")
usuarios = cursor.fetchall()

print("=== USUARIOS EXISTENTES ===")
for usuario in usuarios:
    print(f"ID: {usuario[0]} - Nombre: {usuario[1]}")

# Asignar credenciales al primer usuario (celeste tijaro)
if usuarios:
    user_id = usuarios[0][0]  # ID del primer usuario
    nombre = usuarios[0][1]
    
    # Crear email basado en el nombre
    email = f"{nombre.lower().replace(' ', '.')}@umit.com.co"
    password = "123456"  # Contraseña simple para prueba
    
    # Hash de la contraseña (simple)
    password_hash = hashlib.md5(password.encode()).hexdigest()
    
    # Actualizar el usuario
    cursor.execute("UPDATE usuario SET correo_electronico = ?, password = ? WHERE id_usuario = ?", 
                   (email, password_hash, user_id))
    
    conn.commit()
    
    print(f"\n=== CREDENCIALES ASIGNADAS ===")
    print(f"Usuario: {nombre}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"ID: {user_id}")
    
    print(f"\n✅ Usuario actualizado exitosamente!")
    print(f"Ahora puedes hacer login con:")
    print(f"Email: {email}")
    print(f"Password: {password}")

conn.close()

