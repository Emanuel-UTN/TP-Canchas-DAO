from bd_canchas import crear_tablas
from dao.ClienteDAO.ClienteDAO import ClienteDAO
from models.Cliente.Cliente import Cliente
from dao.conexion import ConexionDB

crear_tablas()

nuevo = Cliente(34443321, "Juan", "Angonese", "3511234567")
ClienteDAO.agregar_cliente(nuevo)

clientes = ClienteDAO.obtener_clientes()
for c in clientes:
    print(c)

ConexionDB().cerrar_conexion()
