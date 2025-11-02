from dao.conexion import ConexionDB

class ServicioCanchaDAO:

    @staticmethod
    def crear_tabla():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ServicioCancha (
                id_servicio INTEGER,
                nro_cancha INTEGER,
                PRIMARY KEY (id_servicio, nro_cancha),
                FOREIGN KEY (id_servicio) REFERENCES Servicio(id_servicio),
                FOREIGN KEY (nro_cancha) REFERENCES Cancha(nro_cancha)
                )
            ''')
        conexion.commit()
        cursor.close()

    @staticmethod
    def agregar_servicio_cancha(id_servicio: int, nro_cancha: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO ServicioCancha (id_servicio, nro_cancha)
            VALUES (?, ?)
        ''', (id_servicio, nro_cancha))
        conexion.commit()
        cursor.close()

    @staticmethod
    def eliminar_servicio_cancha(id_servicio: int, nro_cancha: int):
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM ServicioCancha WHERE id_servicio = ? AND nro_cancha = ?''', (id_servicio, nro_cancha))
        conexion.commit()
        cursor.close()
    
    @staticmethod
    def obtener_servicios_canchas():
        conexion = ConexionDB().obtener_conexion()
        cursor = conexion.cursor()
        servicios_canchas = []
        cursor.execute('''SELECT id_servicio, nro_cancha FROM ServicioCancha''')
        filas = cursor.fetchall()
        for fila in filas:
            servicio_cancha = {
                'id_servicio': fila[0],
                'nro_cancha': fila[1]
            }
            servicios_canchas.append(servicio_cancha)
        cursor.close()
        return servicios_canchas
    