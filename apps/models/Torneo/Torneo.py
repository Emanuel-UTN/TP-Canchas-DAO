from models.Torneo.Equipo import Equipo
from models.Torneo.Partido import Partido
from datetime import datetime

class Torneo:
    def __init__(self, fecha_inicio, fecha_fin, costo_inscripcion, premio):
        self.fecha_inicio = self._validar_fecha_inicio(fecha_inicio)
        self.fecha_fin = self._validar_fecha_fin(fecha_fin, fecha_inicio)
        self.costo_inscripcion = self._validar_costo_inscripcion(costo_inscripcion)
        self.premio = self._validar_premio(premio)
        self.tabla = []
        self.partidos = []
    
    @staticmethod
    def _validar_fecha_inicio(fecha_inicio):
        """Valida la fecha de inicio del torneo."""
        if not fecha_inicio:
            raise ValueError("La fecha de inicio es requerida")
        
        try:
            if isinstance(fecha_inicio, str):
                inicio_obj = datetime.fromisoformat(fecha_inicio.replace('Z', '+00:00'))
            else:
                inicio_obj = fecha_inicio
        except (ValueError, AttributeError):
            raise ValueError("La fecha de inicio no es válida")
        
        ahora = datetime.now()
        if inicio_obj < ahora:
            raise ValueError("La fecha de inicio debe ser una fecha futura")
        
        return fecha_inicio
    
    @staticmethod
    def _validar_fecha_fin(fecha_fin, fecha_inicio):
        """Valida la fecha de fin del torneo."""
        if not fecha_fin:
            raise ValueError("La fecha de fin es requerida")
        
        try:
            if isinstance(fecha_inicio, str) and isinstance(fecha_fin, str):
                inicio = datetime.fromisoformat(fecha_inicio.replace('Z', '+00:00'))
                fin = datetime.fromisoformat(fecha_fin.replace('Z', '+00:00'))
            else:
                inicio = fecha_inicio
                fin = fecha_fin
        except (ValueError, AttributeError):
            raise ValueError("La fecha de fin no es válida")
        
        if fin <= inicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
        
        return fecha_fin
    
    @staticmethod
    def _validar_costo_inscripcion(costo_inscripcion):
        """Valida el costo de inscripción del torneo."""
        try:
            costo = float(costo_inscripcion)
        except (ValueError, TypeError):
            raise ValueError("El costo de inscripción debe ser un número válido")
        
        if costo <= 0:
            raise ValueError("El costo de inscripción debe ser un número positivo")
        
        return costo
    
    @staticmethod
    def _validar_premio(premio):
        """Valida el premio del torneo."""
        try:
            premio_num = float(premio)
        except (ValueError, TypeError):
            raise ValueError("El premio debe ser un número válido")
        
        if premio_num <= 0:
            raise ValueError("El premio debe ser un número positivo")
        
        return premio_num

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