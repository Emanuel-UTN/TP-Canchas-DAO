from bd_canchas import crear_tablas
from dao.conexion import ConexionDB
from apps.models.Gestor import GestorReservas
from apps.dao.CanchaDAO import CanchaDAO
from apps.dao.ReservaDAO import ReservaDAO
from apps.dao.TorneoDAO import TorneoDAO

crear_tablas()
gestor = GestorReservas()

gestor.canchas.extend(CanchaDAO.obtener_canchas())
gestor.reservas.extend(ReservaDAO.obtener_reservas())
gestor.torneos.extend(TorneoDAO.obtener_torneos())

ConexionDB().cerrar_conexion()
