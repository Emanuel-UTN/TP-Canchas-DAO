from flask import Blueprint, jsonify
from dao.ReservaDAO.EstadoReservaDAO import EstadoReservaDAO

bp_estados = Blueprint('estados_reserva', __name__, url_prefix='/api/estados-reserva')

@bp_estados.route('/', methods=['GET'])
def obtener_estados_reserva():
    try:
        estados = EstadoReservaDAO.obtener_estados_reserva()
        return jsonify([{
            'id_estado': e.id_estado,
            'estado': e.estado
        } for e in estados])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
