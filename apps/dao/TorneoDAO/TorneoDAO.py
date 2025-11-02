from dao.conexion import ConexionDB
from models.Torneo.Torneo import Torneo

class TorneoDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Torneo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_inicio DATETIME,
                fecha_fin DATETIME
                costo_inscripcion REAL,
                premio REAL
                )
            ''')
        conexion.commit()
        cursor.close()

    @staticmethod
    def agregar_torneo(torneo: Torneo):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Torneo (fecha_inicio, fecha_fin, costo_inscripcion, premio)
            VALUES (?, ?, ?, ?)
        ''', (torneo.fecha_inicio, torneo.fecha_fin, torneo.costo_inscripcion, torneo.premio))
        conexion.commit()
        cursor.close()

    @staticmethod
    def eliminar_torneo(id_torneo: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM Torneo WHERE id = ?''', (id_torneo,))
        conexion.commit()
        cursor.close()
    
    @staticmethod
    def obtener_torneos():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        torneos = []
        cursor.execute('''SELECT id, fecha_inicio, fecha_fin, costo_inscripcion, premio FROM Torneo''')
        filas = cursor.fetchall()
        for fila in filas:
            torneo = Torneo(
                id=fila[0],
                fecha_inicio=fila[1],
                fecha_fin=fila[2],
                costo_inscripcion=fila[3],
                premio=fila[4]
            )
            torneos.append(torneo)
        cursor.close()
        return torneos

    @staticmethod
    def modificar_torneo(torneo: Torneo):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE Torneo
            SET fecha_inicio = ?, fecha_fin = ?, costo_inscripcion = ?, premio = ?
            WHERE id = ?
        ''', (torneo.fecha_inicio, torneo.fecha_fin, torneo.costo_inscripcion, torneo.premio, torneo.id))
        conexion.commit()
        cursor.close()
    