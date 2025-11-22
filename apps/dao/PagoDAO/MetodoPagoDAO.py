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
                metodo VARCHAR(50) NOT NULL UNIQUE CHECK(length(trim(metodo)) >= 3)
                )
            ''')

        conexion.commit()

        # Seed default payment methods
        cursor.execute('''
            INSERT OR IGNORE INTO MetodoPago (id_metodo_pago, metodo)
            VALUES
                (1, 'Efectivo'),
                (2, 'Mercado Pago')
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
                metodo=fila[1]
            )
            metodos_pago.append(metodo_pago)
        cursor.close()
        return metodos_pago

    @staticmethod
    def obtener_metodo_pago_por_id(id_metodo_pago: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''SELECT id_metodo_pago, metodo FROM MetodoPago WHERE id_metodo_pago = ?''', (id_metodo_pago,))
        fila = cursor.fetchone()
        cursor.close()
        if fila:
            return MetodoPago(
                metodo=fila[1]
            )
        return None

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