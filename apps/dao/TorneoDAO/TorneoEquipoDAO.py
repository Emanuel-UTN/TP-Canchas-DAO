from dao.conexion import ConexionDB

class TorneoEquipoDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TorneoEquipo (
                id_torneo INTEGER NOT NULL CHECK(id_torneo > 0),
                id_equipo INTEGER NOT NULL CHECK(id_equipo > 0),
                puntos INTEGER NOT NULL DEFAULT 0 CHECK(puntos >= 0),
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
    def obtener_tabla_por_torneo(id_torneo: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        tabla = []
        cursor.execute('''SELECT id_equipo, puntos FROM TorneoEquipo WHERE id_torneo = ? ORDER BY puntos DESC''', (id_torneo,))
        filas = cursor.fetchall()
        for fila in filas:
            equipo_puntos = {
                'id_equipo': fila[0],
                'puntos': fila[1]
            }
            tabla.append(equipo_puntos)
        cursor.close()
        return tabla

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

    @staticmethod
    def equipo_en_torneo(id_torneo: int, id_equipo: int) -> bool:
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''SELECT COUNT(*) FROM TorneoEquipo WHERE id_torneo = ? AND id_equipo = ?''', (id_torneo, id_equipo))
        fila = cursor.fetchone()
        cursor.close()
        return fila[0] > 0