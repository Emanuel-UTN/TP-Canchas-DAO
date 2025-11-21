from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
import os

# Agregar el directorio apps al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bd_canchas import crear_tablas
from dao.ClienteDAO.ClienteDAO import ClienteDAO
from dao.CanchaDAO.CanchaDAO import CanchaDAO
from dao.CanchaDAO.TipoCanchaDAO import TipoCanchaDAO
from dao.CanchaDAO.ServicioDAO import ServicioDAO
from dao.ReservaDAO.ReservaDAO import ReservaDAO
from dao.ReservaDAO.EstadoReservaDAO import EstadoReservaDAO
from dao.PagoDAO.PagoDAO import PagoDAO
from dao.PagoDAO.MetodoPagoDAO import MetodoPagoDAO
from dao.TorneoDAO.TorneoDAO import TorneoDAO

from models.Cliente.Cliente import Cliente
from models.Cancha.Cancha import Cancha
from flask import Flask, render_template
from flask_cors import CORS
import sys
import os

# Agregar el directorio apps al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bd_canchas import crear_tablas

app = Flask(__name__)
CORS(app)

# Inicializar tablas al iniciar
crear_tablas()


@app.route('/')
def index():
    return render_template('index.html')


# Registrar blueprints (importar después de crear app y de insertar el path)
from servicios.clientes import bp_clientes
from servicios.canchas import bp_canchas
from servicios.tipos_cancha import bp_tipos
from servicios.servicios import bp_servicios
from servicios.reservas import bp_reservas
from servicios.estados_reserva import bp_estados
from servicios.pagos import bp_pagos
from servicios.metodos_pago import bp_metodos_pago
from servicios.torneos import bp_torneos

app.register_blueprint(bp_clientes)
app.register_blueprint(bp_canchas)
app.register_blueprint(bp_tipos)
app.register_blueprint(bp_servicios)
app.register_blueprint(bp_reservas)
app.register_blueprint(bp_estados)
app.register_blueprint(bp_pagos)
app.register_blueprint(bp_metodos_pago)
app.register_blueprint(bp_torneos)


if __name__ == '__main__':
    app.run(debug=True, port=5000)