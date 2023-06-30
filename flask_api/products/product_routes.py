from flask import Blueprint, jsonify, request, abort, render_template
from functools import wraps

from flask_api.products.product_dao import get_product_dao
from flask_api.auth import jwt_required, admin_required
product_bp = Blueprint('product', __name__, url_prefix='/api/product')
product_dao = get_product_dao()


@product_bp.route('/products', methods=['GET'])
def get_products():
    try:
        productos = product_dao.get_all_products()
        return jsonify({'Productos': [producto.serialize() for producto in productos]}), 200
    except:
        return jsonify({'message': 'No hay productos disponibles'}), 401


@product_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    producto = product_dao.get_product_by_id(id)
    if not producto:
        return jsonify({'message': 'Producto Inexistente'}), 404
    return jsonify({'producto': producto.serialize()}), 200


@product_bp.route('/add_product', methods=['GET', 'POST'])
@jwt_required()
@admin_required()
def create_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        quantity = request.form.get('quantity')
        try:
            producto = product_dao.create_product(name, price, description, quantity)
            # Redirigir a otra página o mostrar mensaje de éxito
            return render_template('add_product.html', success_message='Producto agregado correctamente')
        except ValueError as e:
            return render_template('add_product.html', error=str(e))

    return render_template('add_product.html')


@product_bp.route('/modify_product/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required()
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


@product_bp.route('/del_product/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_product(id):
    producto = product_dao.get_product_by_id(id)
    if not producto:
        return jsonify({'message': 'Producto inexistente'}), 404
    product_dao.delete_product(producto)
    return jsonify({'message': 'Producto eliminado'}), 200
