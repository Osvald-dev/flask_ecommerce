from flask import Blueprint, jsonify, request, abort
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_api.products.product_dao import get_product_dao

product_bp = Blueprint('product', __name__, url_prefix='/api/product')
product_dao = get_product_dao()


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            abort(401, description='Unauthorized')
        return f(*args, **kwargs)
    return decorated_function


@product_bp.route('/products', methods=['GET'])
def get_products():
    try:
        productos = product_dao.get_all_products()
        return jsonify({'Productos': [producto.serialize() for producto in productos]}), 200
    except:
        return jsonify({'message': 'No hay productos disponibles'}), 401

@product_bp.route('/product/<int:id>', methods=['GET'])
def get_by_id(id):
    producto = product_dao.get_product_by_id(id)
    if not producto:
        return jsonify({'message': 'Producto Inexistente'}), 404
    return jsonify({'producto': producto.serialize()}), 200


@product_bp.route('/product', methods=['POST'])
@admin_required
def create_product():
    name = request.json.get('name')
    price = request.json.get('price')
    description = request.json.get('description')
    quantity = request.json.get('quantity')

    try:
        producto = product_dao.create_product(name, price, description, quantity)
        return jsonify({'producto': producto.serialize()}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@product_bp.route('/product/<int:id>', methods=['PUT'])
@admin_required
def update_product(id):
    producto = product_dao.get_product_by_id(id)
    if not producto:
        return jsonify({'message': 'Producto inexistente'}), 404

    name = request.json.get('name', producto.name)
    price = request.json.get('price', producto.price)
    description = request.json.get('description', producto.description)
    quantity = request.json.get('quantity', producto.quantity)

    try:
        producto = product_dao.update_product(id, name, price, description, quantity)
        return jsonify({'producto': producto.serialize()}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@product_bp.route('/product/<int:id>', methods=['DELETE'])
@admin_required
def delete_product(id):
     producto = product_dao.get_product_by_id(id)
     if not producto:
          return jsonify({'message': 'Producto inexistente'}), 404
     product_dao.delete_product(producto)
     return jsonify({'message': 'Producto eliminado'}), 200