from models.Cancha.TipoCancha import TipoCancha
from models.Cancha.Servicio import Servicio

class Cancha:
    def __init__(self, nro_cancha : int, tipo_cancha : TipoCancha, costo_hora : float):
        self.nro_cancha = nro_cancha
        self.tipo_cancha = tipo_cancha
        self.costo_hora = self._validar_costo_hora(costo_hora)
        self.servicios = []
    
    @staticmethod
    def _validar_costo_hora(costo_hora):
        """Valida el costo por hora y retorna el valor si es válido."""
        try:
            costo = float(costo_hora)
        except (ValueError, TypeError):
            raise ValueError("El costo por hora debe ser un número válido")
        
        if costo <= 0:
            raise ValueError("El costo por hora debe ser un número positivo")
        
        return costo

    def agregar_servicio(self, servicio : Servicio):
        self.servicios.append(servicio)
    
    def eliminar_servicio(self, servicio : Servicio):
        if servicio in self.servicios:
            self.servicios.remove(servicio)
    
    def obtener_servicios(self):
        return self.servicios
    
    def obtener_detalles(self):
        return {
            "nro_cancha": self.nro_cancha,
            "tipo_cancha": self.tipo_cancha.tipo,
            "costo_hora": self.costo_hora,
            "servicios": [servicio.servicio for servicio in self.servicios]
        }
    
    def calcular_costo_total(self, horas : int, servicios_a_utilizar : list):
        return self.costo_hora * horas + sum(servicio.costo for servicio in servicios_a_utilizar)
    
    def __str__(self):
        return f"Cancha {self.nro_cancha} - Tipo: {self.tipo_cancha.tipo} - Costo por hora: {self.costo_hora}"