import Equipo
import Partido

class Torneo:
    def __init__(self, fecha_inicio, fecha_fin, costo_inscripcion, premio):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.costo_inscripcion = costo_inscripcion
        self.premio = premio
        self.tabla = []
        self.partidos = []

    def agregar_equipo(self, equipo: Equipo):
        self.tabla.append({equipo: {"puntos": 0, "goles_a_favor": 0, "goles_en_contra": 0}})

    def programar_partido(self, partido: Partido):
        self.partidos.append(partido)

    def actualizar_resultado(self, partido: Partido, goles_equipo_1: int, goles_equipo_2: int):
        partido.finalizar_partido(goles_equipo_1, goles_equipo_2)
        equipo_1 = partido.equipo_1
        equipo_2 = partido.equipo_2

        for equipo_record in self.tabla:
            if equipo_1 in equipo_record:
                equipo_record[equipo_1]["goles_a_favor"] += goles_equipo_1
                equipo_record[equipo_1]["goles_en_contra"] += goles_equipo_2
                if goles_equipo_1 > goles_equipo_2:
                    equipo_record[equipo_1]["puntos"] += 3
                elif goles_equipo_1 == goles_equipo_2:
                    equipo_record[equipo_1]["puntos"] += 1

            if equipo_2 in equipo_record:
                equipo_record[equipo_2]["goles_a_favor"] += goles_equipo_2
                equipo_record[equipo_2]["goles_en_contra"] += goles_equipo_1
                if goles_equipo_2 > goles_equipo_1:
                    equipo_record[equipo_2]["puntos"] += 3
                elif goles_equipo_1 == goles_equipo_2:
                    equipo_record[equipo_2]["puntos"] += 1

    def obtener_informacion(self):
        info = {
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "costo_inscripcion": self.costo_inscripcion,
            "premio": self.premio,
            "numero_equipos": len(self.tabla),
            "numero_partidos": len(self.partidos)
        }
        return info