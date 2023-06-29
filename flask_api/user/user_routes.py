import jwt
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, jsonify, request
from flask_api.config import Config
from flask_api.db import db
from flask_api.user.user_dao import UsuarioDAO

user_bp = Blueprint ('user', __name__, url_prefix='/api/user')
user_dao = UsuarioDAO(db)

@user_bp.route('/allusers', methods=['GET'])
def get_usuarios():
    usuarios = user_dao.list()
    return jsonify({'usuarios': usuarios}), 200

@user_bp.route('/user/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = user_dao.get_id(id)
    return jsonify({'usuario': usuario.serialize()}), 200

@user_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    usuario = user_dao.get_by_email(email)

    if not usuario or not usuario.check_password(password):
        return jsonify({'message': 'Credenciales inválidas'}), 401

    token = jwt.encode({'user_id': usuario.id, 'exp': datetime.utcnow() + timedelta(minutes=30)}, 
                        Config.SECRET_KEY, algorithm='HS256')

    return jsonify({'token': token}), 200

@user_bp.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message':'token de autorization faltante'}),401
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token de autorizacion invalido'}), 401

    if not user_id:
        return jsonify({'message': 'No es posible reconocer su cuenta, intenta logearte nuevamente y vuelve a intentarlo'}), 401
    
    return jsonify({'message': 'Sesión cerrada'}), 200

@user_bp.route('/register', methods=['POST'])
def create_usuario():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    is_admin = request.json.get('is_admin', False)
    try:
        usuario = user_dao.create(username=username, email=email, password=password, is_admin=is_admin)
        return jsonify({'usuario': usuario.serialize()}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    
@user_bp.route('/modify/<int:usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    usuario = user_dao.get_id(usuario_id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    username = request.json.get('username', usuario.username)
    email = request.json.get('email', usuario.email)
    password = request.json.get('password', usuario.password)
    if user_dao.username_exist(username):
        return jsonify({'message': 'El nombre del usuario ya está en uso'})
    try:
        usuario = user_dao.update(id=usuario_id, username=username, email=email, password=password)
        return jsonify({'usuario': usuario.serialize()})
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    
@user_bp.route('/delete/<int:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    usuario = user_dao.get_id(usuario_id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    user_dao.delete_id(usuario_id)
    return jsonify({'message': 'Usuario eliminado correctamente'}), 200