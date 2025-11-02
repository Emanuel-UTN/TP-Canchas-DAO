from dao.conexion import ConexionDB
from models.Pago.MetodoPago import MetodoPago

class MetodoPagoDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS MetodoPago (
                id_metodo_pago INTEGER PRIMARY KEY AUTOINCREMENT,
                metodo TEXT
                )
            ''')

        conexion.commit()
        cursor.close()
    
    @staticmethod
    def agregar_metodo_pago(metodo_pago: MetodoPago):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO MetodoPago (metodo)
            VALUES (?)
        ''', (metodo_pago.metodo,))
        conexion.commit()
        cursor.close()

    @staticmethod
    def eliminar_metodo_pago(id_metodo_pago: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM MetodoPago WHERE id_metodo_pago = ?''', (id_metodo_pago,))
        conexion.commit()
        cursor.close()
    
    @staticmethod
    def obtener_metodos_pago():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        metodos_pago = []
        cursor.execute('''SELECT id_metodo_pago, metodo FROM MetodoPago''')
        filas = cursor.fetchall()
        for fila in filas:
            metodo_pago = MetodoPago(
                id_metodo_pago=fila[0],
                metodo=fila[1]
            )
            metodos_pago.append(metodo_pago)
        cursor.close()
        return metodos_pago

    @staticmethod
    def modificar_metodo_pago(metodo_pago: MetodoPago):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE MetodoPago
            SET metodo = ?
            WHERE id_metodo_pago = ?
        ''', (metodo_pago.metodo, metodo_pago.id_metodo_pago))
        conexion.commit()
        cursor.close()