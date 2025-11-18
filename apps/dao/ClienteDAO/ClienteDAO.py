from dao.conexion import ConexionDB
from models.Cliente.Cliente import Cliente

class ClienteDAO:
    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Cliente (
                dni INTEGER PRIMARY KEY,
                nombre TEXT,
                apellido TEXT,
                telefono TEXT
                )
            ''')
        conexion.commit()
        cursor.close()

    @staticmethod
    def agregar_cliente(cliente: Cliente):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Cliente (dni, nombre, apellido, telefono)
            VALUES (?, ?, ?, ?)
        ''', (cliente.dni, cliente.nombre, cliente.apellido, cliente.telefono))
        conexion.commit()
        cursor.close()
    
    @staticmethod
    def eliminar_cliente(dni: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM Cliente WHERE dni = ?''', (dni,))
        conexion.commit()
        cursor.close()
    
    @staticmethod
    def obtener_clientes():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        clientes = []
        cursor.execute('''SELECT dni, nombre, apellido, telefono FROM Cliente''')
        filas = cursor.fetchall()
        for fila in filas:
            cliente = Cliente(
                dni=fila[0],
                nombre=fila[1],
                apellido=fila[2],
                telefono=fila[3]
            )
            clientes.append(cliente)
        cursor.close()
        return clientes
    
    @staticmethod
    def obtener_cliente_por_dni(dni: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''SELECT dni, nombre, apellido, telefono FROM Cliente WHERE dni = ?''', (dni,))
        fila = cursor.fetchone()
        cursor.close()
        if fila:
            return Cliente(
                dni=fila[0],
                nombre=fila[1],
                apellido=fila[2],
                telefono=fila[3]
            )
        return None
    
    @staticmethod
    def modificar_cliente(cliente: Cliente):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE Cliente
            SET nombre = ?, apellido = ?, telefono = ?
            WHERE dni = ?
        ''', (cliente.nombre, cliente.apellido, cliente.telefono, cliente.dni))
        conexion.commit()
        cursor.close()
