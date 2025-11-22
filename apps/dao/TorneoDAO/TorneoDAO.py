from dao.conexion import ConexionDB
from models.Torneo.Torneo import Torneo
from dao.TorneoDAO.PartidoDAO import PartidoDAO
from dao.TorneoDAO.TorneoEquipoDAO import TorneoEquipoDAO

class TorneoDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Torneo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_inicio DATETIME NOT NULL,
                fecha_fin DATETIME NOT NULL,
                costo_inscripcion REAL NOT NULL CHECK(costo_inscripcion > 0),
                premio REAL NOT NULL CHECK(premio > 0),
                CHECK(fecha_fin > fecha_inicio)
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
                fecha_inicio=fila[1],
                fecha_fin=fila[2],
                costo_inscripcion=fila[3],
                premio=fila[4]
            )
            torneo.id = fila[0]
            torneo.partidos.extend(PartidoDAO.obtener_partidos_por_torneo(torneo.id))
            torneo.tabla.extend(TorneoEquipoDAO.obtener_tabla_por_torneo(torneo.id))
            torneos.append(torneo)
        cursor.close()
        return torneos
    
    @staticmethod
    def obtener_torneo_por_id(id_torneo: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''SELECT id, fecha_inicio, fecha_fin, costo_inscripcion, premio FROM Torneo WHERE id = ?''', (id_torneo,))
        fila = cursor.fetchone()
        torneo = None
        if fila:
            torneo = Torneo(
                fecha_inicio=fila[1],
                fecha_fin=fila[2],
                costo_inscripcion=fila[3],
                premio=fila[4]
            )
            torneo.id = fila[0]
            torneo.partidos.extend(PartidoDAO.obtener_partidos_por_torneo(torneo.id))
            torneo.tabla.extend(TorneoEquipoDAO.obtener_tabla_por_torneo(torneo.id))
        cursor.close()
        return torneo

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

    @staticmethod
    def obtener_detalle_torneo(id_torneo: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('SELECT id, fecha_inicio, fecha_fin, costo_inscripcion, premio FROM Torneo WHERE id = ?', (id_torneo,))
        fila = cursor.fetchone()
        if not fila:
            cursor.close()
            return None

        torneo = Torneo(fecha_inicio=fila['fecha_inicio'],
            fecha_fin=fila['fecha_fin'],
            costo_inscripcion=fila['costo_inscripcion'],
            premio=fila['premio'])
        torneo.id = fila['id']

        # Tabla de posiciones: obtener puntos y estadísticas desde TorneoEquipo y Partido
        cursor.execute('''
            SELECT te.id_equipo, e.nombre, te.puntos,
                (SELECT COUNT(*) FROM Partido p WHERE p.id_torneo = te.id_torneo AND (p.id_equipo1 = te.id_equipo OR p.id_equipo2 = te.id_equipo)) AS partidos_jugados,
                COALESCE((SELECT SUM(CASE WHEN p.id_equipo1 = te.id_equipo THEN p.goles_equipo1 WHEN p.id_equipo2 = te.id_equipo THEN p.goles_equipo2 ELSE 0 END) FROM Partido p WHERE p.id_torneo = te.id_torneo AND (p.id_equipo1 = te.id_equipo OR p.id_equipo2 = te.id_equipo)), 0) AS goles_a_favor,
                COALESCE((SELECT SUM(CASE WHEN p.id_equipo1 = te.id_equipo THEN p.goles_equipo2 WHEN p.id_equipo2 = te.id_equipo THEN p.goles_equipo1 ELSE 0 END) FROM Partido p WHERE p.id_torneo = te.id_torneo AND (p.id_equipo1 = te.id_equipo OR p.id_equipo2 = te.id_equipo)), 0) AS goles_en_contra
            FROM TorneoEquipo te
            JOIN Equipo e ON te.id_equipo = e.id_equipo
            WHERE te.id_torneo = ?
            ORDER BY te.puntos DESC, goles_a_favor - goles_en_contra DESC
        ''', (id_torneo,))

        
        filas = cursor.fetchall()
        posicion = 1
        for f in filas:
            torneo.tabla.append({
                'posicion': posicion,
                'id_equipo': f['id_equipo'],
                'nombre': f['nombre'],
                'puntos': f['puntos'],
                'partidos_jugados': f['partidos_jugados'],
                'goles_a_favor': f['goles_a_favor'],
                'goles_en_contra': f['goles_en_contra']
            })
            posicion += 1

        # Próximos partidos: listar con nombres de equipos y cancha
        cursor.execute('''
            SELECT p.id_partido, p.id_equipo1, e1.nombre AS equipo1_nombre, p.id_equipo2, e2.nombre AS equipo2_nombre,
                   p.nro_cancha, tc.tipo AS cancha_tipo, p.fecha_hora, p.goles_equipo1, p.goles_equipo2
            FROM Partido p
            JOIN Equipo e1 ON p.id_equipo1 = e1.id_equipo
            JOIN Equipo e2 ON p.id_equipo2 = e2.id_equipo
            LEFT JOIN Cancha c ON p.nro_cancha = c.nro_cancha
            LEFT JOIN TipoCancha tc ON c.id_tipo = tc.id_tipo
            WHERE p.id_torneo = ?
            ORDER BY p.fecha_hora ASC
        ''', (id_torneo,))

        for pf in cursor.fetchall():
            torneo.partidos.append({
                'id_partido': pf['id_partido'],
                'equipo1_id': pf['id_equipo1'],
                'equipo1_nombre': pf['equipo1_nombre'],
                'equipo2_id': pf['id_equipo2'],
                'equipo2_nombre': pf['equipo2_nombre'],
                'nro_cancha': pf['nro_cancha'],
                'cancha_tipo': pf['cancha_tipo'],
                'fecha_hora': pf['fecha_hora'],
                'goles_equipo1': pf['goles_equipo1'],
                'goles_equipo2': pf['goles_equipo2']
            })

        cursor.close()
        return torneo

    @staticmethod
    def listar_torneos_con_cantidad_equipos():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            SELECT t.id, t.fecha_inicio, t.fecha_fin, t.costo_inscripcion, t.premio,
                (SELECT COUNT(*) FROM TorneoEquipo te WHERE te.id_torneo = t.id) AS numero_equipos
            FROM Torneo t
        ''')
        filas = cursor.fetchall()
        torneos = []
        for f in filas:
            torneos.append({
                'id': f['id'],
                'fecha_inicio': f['fecha_inicio'],
                'fecha_fin': f['fecha_fin'],
                'costo_inscripcion': f['costo_inscripcion'],
                'premio': f['premio'],
                'numero_equipos': f['numero_equipos']
            })
        cursor.close()
        return torneos
    