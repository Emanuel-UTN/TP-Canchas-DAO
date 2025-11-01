import Equipo
from apps.models.Cancha import Cancha

class Partido:
    def __init__(self, equipo_1: Equipo, equipo_2: Equipo, fecha_hora: str, cancha: Cancha):
        self.equipo_1 = equipo_1
        self.equipo_2 = equipo_2
        self.cancha = cancha
        self.fecha_hora = fecha_hora
    
    def finalizar_partido(self, goles_1: int, goles_2: int):
        self.goles_1, self.goles_2 = goles_1, goles_2

    def obtener_resultado(self) -> str:
        return f"{self.equipo_1.nombre} {self.goles_1} - {self.goles_2} {self.equipo_2.nombre}"
    
    def obtener_ganador(self) -> Equipo:
        if self.goles_1 > self.goles_2:
            return self.equipo_1
        elif self.goles_2 > self.goles_1:
            return self.equipo_2
        else:
            return None  # Empate
        
    def obtener_perdedor(self) -> Equipo:
        if self.goles_1 < self.goles_2:
            return self.equipo_1
        elif self.goles_2 < self.goles_1:
            return self.equipo_2
        else:
            return None  # Empate
        
    def __str__(self):
        return f"Partido: {self.equipo_1.nombre} vs {self.equipo_2.nombre} en {self.cancha.nombre} el {self.fecha_hora}"