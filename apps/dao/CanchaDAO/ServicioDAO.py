from dao.conexion import ConexionDB
from models.Cancha.Servicio import Servicio

class ServicioDAO:

    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Servicio (
                id_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
                servicio TEXT,
                costo REAL
                )
            ''')

        conexion.commit()
        cursor.close()
        
    @staticmethod
    def agregar_servicio(servicio: Servicio):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Servicio (servicio, costo)
            VALUES (?, ?)
        ''', (servicio.servicio, servicio.costo))
        conexion.commit()
        cursor.close()
    
    @staticmethod
    def eliminar_servicio(id_servicio: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM Servicio WHERE id_servicio = ?''', (id_servicio,))
        conexion.commit()
        cursor.close()

    @staticmethod
    def obtener_servicios():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        servicios = []
        cursor.execute('''SELECT id_servicio, servicio, costo FROM Servicio''')
        filas = cursor.fetchall()
        for fila in filas:
            servicio = Servicio(
                id_servicio=fila[0],
                servicio=fila[1],
                costo=fila[2]
            )
            servicios.append(servicio)
        cursor.close()
        return servicios

    @staticmethod
    def modificar_servicio(servicio: Servicio):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE Servicio
            SET servicio = ?, costo = ?
            WHERE id_servicio = ?
        ''', (servicio.servicio, servicio.costo, servicio.id_servicio))
        conexion.commit()
        cursor.close()