from dao.conexion import ConexionDB
from models.Torneo.Equipo import Equipo

class EquipoDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Equipo (
                id_equipo INTEGER PRIMARY KEY AUTOINCREMENT,
                dni_delegado TEXT,
                nombre VARCHAR(50)
                )
            ''')
    
        conexion.commit()
        cursor.close()

    @staticmethod
    def agregar_equipo(equipo: Equipo):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Equipo (dni_delegado, nombre)
            VALUES (?, ?)
        ''', (equipo.dni_delegado, equipo.nombre))
        conexion.commit()
        cursor.close()
    
    @staticmethod
    def eliminar_equipo(id_equipo: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM Equipo WHERE id_equipo = ?''', (id_equipo,))
        conexion.commit()
        cursor.close()
    
    @staticmethod
    def obtener_equipos():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        equipos = []
        cursor.execute('''SELECT id_equipo, dni_delegado, nombre FROM Equipo''')
        filas = cursor.fetchall()
        for fila in filas:
            equipo = Equipo(
                id_equipo=fila[0],
                dni_delegado=fila[1],
                nombre=fila[2]
            )
            equipos.append(equipo)
        cursor.close()
        return equipos
    
    @staticmethod
    def modificar_equipo(equipo: Equipo):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE Equipo
            SET dni_delegado = ?, nombre = ?
            WHERE id_equipo = ?
        ''', (equipo.dni_delegado, equipo.nombre, equipo.id_equipo))
        conexion.commit()
        cursor.close()