from flask import Blueprint, jsonify, request
from dao.PagoDAO.PagoDAO import PagoDAO
from dao.PagoDAO.MetodoPagoDAO import MetodoPagoDAO
from models.Pago.Pago import Pago
from models.Pago.MetodoPago import MetodoPago

bp_pagos = Blueprint('pagos', __name__, url_prefix='/api/pagos')

@bp_pagos.route('/', methods=['GET'])
def obtener_pagos():
    try:
        pagos = PagoDAO.obtener_pagos()
        return jsonify([{
            'id_pago': p.id_pago,
            'id_metodo_pago': p.id_metodo_pago,
            'fecha_hora': p.fecha_hora,
            'monto': p.monto
        } for p in pagos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_pagos.route('/', methods=['POST'])
def agregar_pago():
    try:
        data = request.json
        metodo_placeholder = MetodoPago("")
        pago = Pago(
            metodo_pago=metodo_placeholder,
            fecha_hora=data['fecha_hora'],
            monto=data['monto']
        )
        pago.id_metodo_pago = data.get('id_metodo_pago')
        pago.id_pago = None
        PagoDAO.agregar_pago(pago)
        return jsonify({'mensaje': 'Pago agregado exitosamente'}), 201
    except ValueError as e:
        # Error de validación del modelo
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        return jsonify({'error': f'Campo requerido faltante: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
