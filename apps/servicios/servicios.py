from flask import Blueprint, jsonify, request
from dao.CanchaDAO.ServicioDAO import ServicioDAO
from models.Cancha.Servicio import Servicio

bp_servicios = Blueprint('servicios', __name__, url_prefix='/api/servicios')

@bp_servicios.route('/', methods=['GET'])
def obtener_servicios():
    try:
        servicios = ServicioDAO.obtener_servicios()
        return jsonify([{
            'id_servicio': s.id_servicio,
            'servicio': s.servicio,
            'costo': s.costo
        } for s in servicios])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_servicios.route('/', methods=['POST'])
def agregar_servicio():
    try:
        data = request.json
        servicio = Servicio(
            servicio=data['servicio'],
            costo=data['costo']
        )
        ServicioDAO.agregar_servicio(servicio)
        return jsonify({'mensaje': 'Servicio agregado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
