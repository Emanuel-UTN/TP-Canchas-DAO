from flask import Blueprint, jsonify, request
from dao.TorneoDAO.TorneoDAO import TorneoDAO
from models.Torneo.Torneo import Torneo

bp_torneos = Blueprint('torneos', __name__, url_prefix='/api/torneos')

@bp_torneos.route('/', methods=['GET'])
def obtener_torneos():
    try:
        torneos = TorneoDAO.obtener_torneos()
        return jsonify([{
            'id': t.id,
            'fecha_inicio': t.fecha_inicio,
            'fecha_fin': t.fecha_fin,
            'costo_inscripcion': t.costo_inscripcion,
            'premio': t.premio
        } for t in torneos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_torneos.route('/', methods=['POST'])
def agregar_torneo():
    try:
        data = request.json
        torneo = Torneo(
            fecha_inicio=data['fecha_inicio'],
            fecha_fin=data['fecha_fin'],
            costo_inscripcion=data['costo_inscripcion'],
            premio=data['premio']
        )
        TorneoDAO.agregar_torneo(torneo)
        return jsonify({'mensaje': 'Torneo agregado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp_torneos.route('/<int:id>', methods=['PUT'])
def modificar_torneo(id):
    try:
        data = request.json
        torneo = Torneo(
            fecha_inicio=data['fecha_inicio'],
            fecha_fin=data['fecha_fin'],
            costo_inscripcion=data['costo_inscripcion'],
            premio=data['premio']
        )
        torneo.id = id
        TorneoDAO.modificar_torneo(torneo)
        return jsonify({'mensaje': 'Torneo modificado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp_torneos.route('/<int:id>', methods=['DELETE'])
def eliminar_torneo(id):
    try:
        TorneoDAO.eliminar_torneo(id)
        return jsonify({'mensaje': 'Torneo eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
