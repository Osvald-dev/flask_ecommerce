from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_api.cart.cart_dao import CartDao
from flask_api.user.user_model import User
from flask_api.db import db

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')
cart_dao = CartDao(db)

@cart_bp.route('/cart', methods=['POST'])
@jwt_required()
def create_cart():
    current_user_id = get_jwt_identity()
    user = User.get_by_id(current_user_id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    cart = cart_dao.create_cart(user_id=user.id)
    return jsonify({'cart_id': cart.id, 'user_id': cart.user_id}), 201

@cart_bp.route('/cart/<int:cart_id>', methods=['GET'])
@jwt_required()
def get_cart_by_id(cart_id):
    current_user_id = get_jwt_identity()
    user = User.get_by_id(current_user_id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    cart = cart_dao.get_cart_by_id(cart_id=cart_id)
    if not cart:
        return jsonify({'message': 'Carrito no encontrado'}), 404
    if cart.user_id != user.id:
        return jsonify({'message': 'No tienes acceso a este carrito'}), 403
    return jsonify({'cart_id': cart.id, 'user_id': cart.user_id, 'products': cart.products}), 200

@cart_bp.route('/cart/<int:cart_id>/add-product/<int:product_id>', methods=['POST'])
@jwt_required()
def add_product_to_cart(cart_id, product_id):
    current_user_id = get_jwt_identity()
    user = User.get_by_id(current_user_id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    cart = cart_dao.get_cart_by_id(cart_id=cart_id)
    if not cart:
        return jsonify({'message': 'Carrito no encontrado'}), 404
    if cart.user_id != user.id:
        return jsonify({'message': 'No tienes acceso a este carrito'}), 403
    cart_dao.add_product_to_cart(cart_id=cart_id, product_id=product_id)
    return jsonify({'message': 'Producto añadido exitosamente al carrito'}), 201

