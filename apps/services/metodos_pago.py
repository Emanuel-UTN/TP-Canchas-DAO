from flask import Blueprint, jsonify, request
from dao.PagoDAO.MetodoPagoDAO import MetodoPagoDAO
from models.Pago.MetodoPago import MetodoPago

bp_metodos_pago = Blueprint('metodos_pago', __name__, url_prefix='/api/metodos-pago')

@bp_metodos_pago.route('/', methods=['GET'])
def obtener_metodos_pago():
    try:
        metodos = MetodoPagoDAO.obtener_metodos_pago()
        return jsonify([{
            'metodo': m.metodo
        } for m in metodos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_metodos_pago.route('/', methods=['POST'])
def agregar_metodo_pago():
    try:
        data = request.json
        metodo_pago = MetodoPago(metodo=data['metodo'])
        MetodoPagoDAO.agregar_metodo_pago(metodo_pago)
        return jsonify({'mensaje': 'Método de pago agregado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
