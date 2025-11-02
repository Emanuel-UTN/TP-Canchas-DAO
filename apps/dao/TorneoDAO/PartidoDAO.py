from dao.conexion import ConexionDB
from models.Torneo.Partido import Partido

class PartidoDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Partido (
                id_partido INTEGER PRIMARY KEY AUTOINCREMENT,
                id_torneo INTEGER,
                id_equipo1 INTEGER,
                id_equipo2 INTEGER,
                nro_cancha INTEGER,
                goles_equipo1 INTEGER,
                goles_equipo2 INTEGER,
                fecha_hora DATETIME,
                FOREIGN KEY (id_torneo) REFERENCES Torneo(id),
                FOREIGN KEY (id_equipo1) REFERENCES Equipo(id_equipo),
                FOREIGN KEY (id_equipo2) REFERENCES Equipo(id_equipo),
                FOREIGN KEY (nro_cancha) REFERENCES Cancha(nro_cancha)
                )
            ''')

        conexion.commit()
        cursor.close()

    @staticmethod
    def agregar_partido(partido: Partido):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Partido (id_torneo, id_equipo1, id_equipo2, nro_cancha, goles_equipo1, 
                    goles_equipo2, fecha_hora)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (partido.id_torneo, partido.id_equipo1, partido.id_equipo2, partido.nro_cancha, 
            partido.goles_equipo1, partido.goles_equipo2, partido.fecha_hora))
        conexion.commit()
        cursor.close()

    @staticmethod
    def eliminar_partido(id_partido: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM Partido WHERE id_partido = ?''', (id_partido,))
        conexion.commit()
        cursor.close()
    
    @staticmethod
    def obtener_partidos():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        partidos = []
        cursor.execute('''SELECT id_partido, id_torneo, id_equipo1, id_equipo2, nro_cancha, 
                goles_equipo1, goles_equipo2, fecha_hora FROM Partido''')
        filas = cursor.fetchall()
        for fila in filas:
            partido = Partido(
                id_partido=fila[0],
                id_torneo=fila[1],
                id_equipo1=fila[2],
                id_equipo2=fila[3],
                nro_cancha=fila[4],
                goles_equipo1=fila[5],
                goles_equipo2=fila[6],
                fecha_hora=fila[7]
            )
            partidos.append(partido)
        cursor.close()
        return partidos
    
    @staticmethod
    def modificar_partido(partido: Partido):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE Partido
            SET id_torneo = ?, id_equipo1 = ?, id_equipo2 = ?, nro_cancha = ?, 
                goles_equipo1 = ?, goles_equipo2 = ?, fecha_hora = ?
            WHERE id_partido = ?''',
            (partido.id_torneo, partido.id_equipo1, partido.id_equipo2, partido.nro_cancha, 
            partido.goles_equipo1, partido.goles_equipo2, partido.fecha_hora, partido.id_partido))
        conexion.commit()
        cursor.close()
    