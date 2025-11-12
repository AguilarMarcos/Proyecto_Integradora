from database import crear_conexion
from mysql.connector import Error

def ver_usuario():
    conexion = crear_conexion()
    if not conexion:
        return []
    
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, username FROM usuarios")
        resultado = cursor.fetchall()
        return resultado
    except Error as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def crear_usuarios(username, password):
    conexion = crear_conexion()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        consulta = "INSERT INTO usuarios (username, password) VALUES (%s, %s)"
        cursor.execute(consulta, (username, password))
        conexion.commit()
        return True
    except Error as e:
        print(f"Error al crear usuario: {e}")
        return False
    finally:
        if conexion and conexion.is_connected():
            conexion.close()


def actualizar_usuarios(id_usuario, new_username, new_password):
    conexion = crear_conexion()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        consulta = "UPDATE usuarios SET username = %s, password = %s WHERE id = %s"
        cursor.execute(
            consulta,
            (new_username, new_password, id_usuario)
        )
        conexion.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error al actualizar usuario: {e}")
        return False
    finally:
        if conexion and conexion.is_connected():
            conexion.close()


def eliminar_usuario(id_usuario):
    conexion = crear_conexion()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        consulta = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(consulta, (id_usuario,))
        conexion.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error al eliminar usuario: {e}")
        return False
    finally:
        if conexion and conexion.is_connected():
            conexion.close()