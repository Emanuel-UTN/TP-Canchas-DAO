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
    """Dashboard mínimo: enlaces a vistas modulares sin duplicar formularios."""
    return render_template('index.html')

# Rutas HTML modulares (evitan duplicación en index)
@app.route('/clientes')
def page_clientes():
    return render_template('clientes.html', active_tab='clientes')

@app.route('/canchas')
def page_canchas():
    return render_template('canchas.html', active_tab='canchas')

@app.route('/reservas')
def page_reservas():
    return render_template('reservas.html', active_tab='reservas')

@app.route('/pagos')
def page_pagos():
    return render_template('pagos.html', active_tab='pagos')

@app.route('/torneos')
def page_torneos():
    return render_template('torneos.html', active_tab='torneos')

@app.route('/tipos-cancha')
def page_tipos_cancha():
    return render_template('tipos-cancha.html', active_tab='tipos-cancha')

@app.route('/servicios')
def page_servicios():
    return render_template('servicios.html', active_tab='servicios')

@app.route('/metodos-pago')
def page_metodos_pago():
    return render_template('metodos-pago.html', active_tab='metodos-pago')


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