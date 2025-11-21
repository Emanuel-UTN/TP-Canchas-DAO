from flask import Blueprint, jsonify, request
from dao.ClienteDAO.ClienteDAO import ClienteDAO
from models.Cliente.Cliente import Cliente

bp_clientes = Blueprint('clientes', __name__, url_prefix='/api/clientes')

@bp_clientes.route('/', methods=['GET'])
def obtener_clientes():
    try:
        clientes = ClienteDAO.obtener_clientes()
        return jsonify([{
            'dni': c.dni,
            'nombre': c.nombre,
            'apellido': c.apellido,
            'telefono': c.telefono
        } for c in clientes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp_clientes.route('/', methods=['POST'])
def agregar_cliente():
    try:
        data = request.json
        cliente = Cliente(
            dni=data['dni'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            telefono=data['telefono']
        )
        ClienteDAO.agregar_cliente(cliente)
        return jsonify({'mensaje': 'Cliente agregado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp_clientes.route('/<int:dni>', methods=['GET'])
def obtener_cliente_por_dni(dni):
    try:
        cliente = ClienteDAO.obtener_cliente_por_dni(dni)
        
        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404

        return jsonify({
            'dni': cliente.dni,
            'nombre': cliente.nombre,
            'apellido': cliente.apellido,
            'telefono': cliente.telefono
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp_clientes.route('/<int:dni>', methods=['PUT'])
def modificar_cliente(dni):
    try:
        data = request.json
        cliente = Cliente(
            dni=dni,
            nombre=data['nombre'],
            apellido=data['apellido'],
            telefono=data['telefono']
        )
        ClienteDAO.modificar_cliente(cliente)
        return jsonify({'mensaje': 'Cliente modificado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp_clientes.route('/<int:dni>', methods=['DELETE'])
def eliminar_cliente(dni):
    try:
        ClienteDAO.eliminar_cliente(dni)
        return jsonify({'mensaje': 'Cliente eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
