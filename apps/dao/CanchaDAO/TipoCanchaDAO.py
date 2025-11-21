from dao.conexion import ConexionDB
from models.Cancha.TipoCancha import TipoCancha

class TipoCanchaDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TipoCancha (
                id_tipo INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT
                )
            ''')
        # índice único para garantizar que no se repita el nombre
        cursor.execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_tipo_cancha_unico ON TipoCancha(tipo);''')

        conexion.commit()
        cursor.close()
    
    @staticmethod
    def agregar_tipo_cancha(tipo_cancha: TipoCancha):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO TipoCancha (tipo)
            VALUES (?)
        ''', (tipo_cancha.tipo,))
        conexion.commit()
        cursor.close()

    @staticmethod
    def eliminar_tipo_cancha(id_tipo: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM TipoCancha WHERE id_tipo = ?''', (id_tipo,))
        conexion.commit()
        cursor.close()
    
    @staticmethod
    def obtener_tipos_cancha():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        tipos_cancha = []
        cursor.execute('''SELECT id_tipo, tipo FROM TipoCancha''')
        filas = cursor.fetchall()
        for fila in filas:
            tipo_cancha = TipoCancha(
                tipo=fila[1]
            )
            tipos_cancha.append(tipo_cancha)
        cursor.close()
        return tipos_cancha

    @staticmethod
    def obtener_tipo_cancha_por_nombre(nombre: str):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''SELECT tipo FROM TipoCancha WHERE tipo = ?''', (nombre,))
        fila = cursor.fetchone()
        cursor.close()
        return TipoCancha(tipo=fila[0]) if fila else None
    
    @staticmethod
    def obtener_tipo_cancha_por_id(id_tipo: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''SELECT id_tipo, tipo FROM TipoCancha WHERE id_tipo = ?''', (id_tipo,))
        fila = cursor.fetchone()
        tipo_cancha = None
        if fila:
            tipo_cancha = TipoCancha(
                tipo=fila[1]
            )
        cursor.close()
        return tipo_cancha
    
    @staticmethod
    def obtener_id_tipo_cancha_por_tipo(tipo: str):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''SELECT id_tipo, tipo FROM TipoCancha WHERE tipo = ?''', (tipo,))
        fila = cursor.fetchone()
        cursor.close()
        return fila[0] if fila else None

    @staticmethod
    def modificar_tipo_cancha_por_nombre(nombre_actual: str, nuevo_nombre: str):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''UPDATE TipoCancha SET tipo = ? WHERE tipo = ?''', (nuevo_nombre, nombre_actual))
        conexion.commit()
        cursor.close()

    @staticmethod
    def eliminar_tipo_cancha_por_nombre(nombre: str):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM TipoCancha WHERE tipo = ?''', (nombre,))
        conexion.commit()
        cursor.close()