from dao.conexion import ConexionDB
from models.Cancha.Cancha import Cancha

class CanchaDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Cancha (
                nro_cancha INTEGER PRIMARY KEY AUTOINCREMENT,
                id_tipo INTEGER,
                costo_por_hora REAL,
                FOREIGN KEY (id_tipo) REFERENCES TipoCancha(id_tipo)
                )
            ''')
        conexion.commit()
        cursor.close()
        
    @staticmethod
    def agregar_cancha(cancha: Cancha):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Cancha (id_tipo, costo_por_hora)
            VALUES (?, ?)
        ''', (cancha.id_tipo, cancha.costo_por_hora))
        conexion.commit()
        cursor.close()
    
    @staticmethod
    def eliminar_cancha(nro_cancha: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM Cancha WHERE nro_cancha = ?''', (nro_cancha,))
        conexion.commit()
        cursor.close()

    @staticmethod
    def obtener_canchas():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        canchas = []
        cursor.execute('''SELECT nro_cancha, id_tipo, costo_por_hora FROM Cancha''')
        filas = cursor.fetchall()
        for fila in filas:
            cancha = Cancha(
                nro_cancha=fila[0],
                id_tipo=fila[1],
                costo_por_hora=fila[2]
            )
            canchas.append(cancha)
        cursor.close()
        return canchas

    @staticmethod
    def modificar_cancha(cancha: Cancha):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE Cancha
            SET id_tipo = ?, costo_por_hora = ?
            WHERE nro_cancha = ?
        ''', (cancha.id_tipo, cancha.costo_por_hora, cancha.nro_cancha))
        conexion.commit()
        cursor.close()

