from database import crear_conexion
from mysql.connector import Error

def ver_pedido():
    conexion = crear_conexion()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.id_pedido,
                   p.nombre_cliente,
                   p.fecha_entrega,
                   p.descripcion,
                   p.precio_total,
                   p.abono,
                   u.username AS empleado
            FROM pedidos p
            JOIN usuarios u ON p.id_empleado = u.id
        """)
        
        return cursor.fetchall()

    except Error as e:
        print(f"Error al obtener pedidos: {e}")
        return []

    finally:
        if conexion and conexion.is_connected():
            conexion.close()



def crear_pedido(nombre_cliente, fecha_entega, descripcion, precio_total, abono, id_empleado):
    """Crea un nuevo pedido en la base de datos."""
    conexion = crear_conexion()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO pedidos (nombre_cliente, descripcion, fecha_entrega, precio_total, abono, id_empleado)
            VALUES (%s, %s,%s, %s, %s, %s)
        """, (nombre_cliente, descripcion, fecha_entega, precio_total, abono, id_empleado))

        conexion.commit()
        return True

    except Exception as e:
        print(f"Error al crear pedido: {e}")
        return False

    finally:
        if conexion and conexion.is_connected():
            conexion.close()


def obtener_pedido_por_id(id_pedido):
    conexion = crear_conexion()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM pedidos WHERE id_pedido = %s
        """, (id_pedido,))
        return cursor.fetchone()
        
    except Exception as e:
        print("Error al obtener pedido:", e)
        return None

    finally:
        if conexion.is_connected():
            conexion.close()


def actualizar_pedido(id_pedido, nombre_cliente, fecha_entrega, descripcion, precio_total, abono, id_empleado):
    conexion = crear_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor(dictionary=True)

        
        cursor.execute("SELECT abono FROM pedidos WHERE id_pedido = %s", (id_pedido,))
        resultado = cursor.fetchone()

        if not resultado:
            return False

        abono_anterior = float(resultado["abono"])
        nuevo_abono_total = abono_anterior + float(abono)


        cursor.execute("""
            UPDATE pedidos 
            SET nombre_cliente = %s,
                fecha_entrega = %s,
                descripcion = %s,
                precio_total = %s,
                abono = %s,
                id_empleado = %s
            WHERE id_pedido = %s
        """, (nombre_cliente, fecha_entrega, descripcion, precio_total, nuevo_abono_total, id_empleado, id_pedido))

        conexion.commit()
        return True

    except Exception as e:
        print("Error al actualizar pedido:", e)
        return False

    finally:
        if conexion.is_connected():
            conexion.close()




def eliminar_pedido(id_pedido):
    """Elimina un pedido por su ID."""
    conexion = crear_conexion()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM pedidos WHERE id_pedido = %s", (id_pedido,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar pedido: {e}")
        return False
    finally:
        if conexion and conexion.is_connected():
            conexion.close()
