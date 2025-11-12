from database import crear_conexion
from mysql.connector import Error

def validar_credenciales(usuario, password):
    conexion = crear_conexion() 
    if not conexion:
        return False
    cursor = None
    try:
        cursor = conexion.cursor()
        consulta = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
        cursor.execute(consulta, (usuario, password))
        resultado = cursor.fetchone()
        
        return bool(resultado)
    except Error as e:
        print(f"Error en la validación de credenciales: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()