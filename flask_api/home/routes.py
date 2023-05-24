from flask import Blueprint, jsonify

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
def home():
        response = {'message': 'Home'}
        return jsonify(response), 200  
