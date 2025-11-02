import sqlite3
from dao.CanchaDAO.CanchaDAO import CanchaDAO
from dao.CanchaDAO.ServicioDAO import ServicioDAO
from dao.CanchaDAO.TipoCanchaDAO import TipoCanchaDAO
from dao.CanchaDAO.ServicioCanchaDAO import ServicioCanchaDAO

from dao.ClienteDAO.ClienteDAO import ClienteDAO

from dao.PagoDAO.PagoDAO import PagoDAO
from dao.PagoDAO.MetodoPagoDAO import MetodoPagoDAO

from dao.ReservaDAO.ReservaDAO import ReservaDAO  
from dao.ReservaDAO.EstadoReservaDAO import EstadoReservaDAO

from dao.TorneoDAO.TorneoDAO import TorneoDAO
from dao.TorneoDAO.EquipoDAO import EquipoDAO
from dao.TorneoDAO.TorneoEquipoDAO import TorneoEquipoDAO
from dao.TorneoDAO.PartidoDAO import PartidoDAO



def crear_tablas():
    
    #Tabla TipoCancha
    TipoCanchaDAO.crear_tabla()
    #Tabla Servicio
    ServicioDAO.crear_tabla()
    #Tabla Torneo
    TorneoDAO.crear_tabla()
    #Tabla MetodoPago
    MetodoPagoDAO.crear_tabla()
    #Tabla Pago
    PagoDAO.crear_tabla()
    #Tabla Cancha
    CanchaDAO.crear_tabla()
    #Tabla Cliente
    ClienteDAO.crear_tabla()
    #Tabla EstadoReserva
    EstadoReservaDAO.crear_tabla()
    #Tabla ServicioCancha
    ServicioCanchaDAO.crear_tabla()
    #Tabla Equipo
    EquipoDAO.crear_tabla()
    #Tabla TorneoEquipo
    TorneoEquipoDAO.crear_tabla()
    #Tabla Partido
    PartidoDAO.crear_tabla()
    #Tabla Reserva
    ReservaDAO.crear_tabla()


