from dao.conexion import ConexionDB

class TorneoEquipoDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TorneoEquipo (
                id_torneo INTEGER,
                id_equipo INTEGER,
                puntos INTEGER,
                PRIMARY KEY (id_torneo, id_equipo),
                FOREIGN KEY (id_torneo) REFERENCES Torneo(id),
                FOREIGN KEY (id_equipo) REFERENCES Equipo(id_equipo)
                )
            ''')
        conexion.commit()
        cursor.close()

    @staticmethod
    def agregar_torneo_equipo(id_torneo: int, id_equipo: int, puntos: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO TorneoEquipo (id_torneo, id_equipo, puntos)
            VALUES (?, ?, ?)
        ''', (id_torneo, id_equipo, puntos))
        conexion.commit()
        cursor.close()

    @staticmethod
    def eliminar_torneo_equipo(id_torneo: int, id_equipo: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM TorneoEquipo WHERE id_torneo = ? AND id_equipo = ?''', (id_torneo, id_equipo))
        conexion.commit()
        cursor.close()

    @staticmethod
    def obtener_torneos_equipos():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        torneos_equipos = []
        cursor.execute('''SELECT id_torneo, id_equipo, puntos FROM TorneoEquipo''')
        filas = cursor.fetchall()
        for fila in filas:
            torneo_equipo = {
                'id_torneo': fila[0],
                'id_equipo': fila[1],
                'puntos': fila[2]
            }
            torneos_equipos.append(torneo_equipo)
        cursor.close()
        return torneos_equipos

    @staticmethod
    def modificar_torneo_equipo(id_torneo: int, id_equipo: int, puntos: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE TorneoEquipo
            SET puntos = ?
            WHERE id_torneo = ? AND id_equipo = ?
        ''', (puntos, id_torneo, id_equipo))
        conexion.commit()
        cursor.close()