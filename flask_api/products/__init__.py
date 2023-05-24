from flask import Blueprint
from .product_routes import product_bp
from .product_model import Product
from .product_dao import ProductDAO
# from db import db