import TipoCancha
import Servicio

class Cancha:
    def __init__(self, nro_cancha : int, tipo_cancha : TipoCancha, costo_hora : float):
        self.nro_cancha = nro_cancha
        self.tipo_cancha = tipo_cancha
        self.costo_hora = costo_hora
        self.servicios = []

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
            "tipo_cancha": self.tipo_cancha.nombre,
            "costo_hora": self.costo_hora,
            "servicios": [servicio.nombre for servicio in self.servicios]
        }
    
    def calcular_costo_total(self, horas : int, servicios_a_utilizar : list):
        return self.costo_hora * horas + sum(servicio.costo for servicio in servicios_a_utilizar)
    
    def __str__(self):
        return f"Cancha {self.nro_cancha} - Tipo: {self.tipo_cancha.nombre} - Costo por hora: {self.costo_hora}"