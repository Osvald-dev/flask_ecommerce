from flask import g, current_app
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List
from .product_model import Product
from flask_api.cart.cart_model import Cart
from flask_api.db import db


class ProductDAO:

    def __init__(self, db):
        self.db = db
        self.session = db.session

    def close_session(self, exception=None):
        session = getattr(g, '_session', None)
        if session is not None:
            session.close()

    def get_all_products(self)-> List[Product]:
        return self.session.query(Product).all()
    
    def get_product_by_id(self, product_id: int)-> Product:
        return self.session.query(Product).filter_by(id=product_id).first()
    
    def add_product_to_cart(self, product_id: int, cart_id: int, quantity: int)-> Cart:
        cart = self.session.query(Cart).filter_by(id=cart_id).first()
        product = self.session.query(Product).filter_by(id=product_id).first()
        product.quantity -= quantity
        cart.Product.append(product)
        self.session.commit()
        return cart

    def create_product(self, product: Product)-> Product:
        self.session.add(product)
        self.session.commit()
        return product
    
    def update_product(self, product_id: int, product: Product)-> Product:
        product_to_update = self.session.query(Product).filter_by(id=product_id).first()
        product_to_update.product = product.product
        product_to_update.price = product.price
        product_to_update.description = product.description
        product_to_update.quantity = product.quantity
        self.session.commit()
        return product_to_update
    
    def delete_product(self, product_id: int) -> None:
        product_to_delete = self.session.query(Product).filter_by(id=product_id).first()
        self.session.delete(product_to_delete)
        self.session.commit()
        return product_to_delete
    
    def shutdown_session(exception=None):
        db = getattr(g, '_database', None)
        if db is not None:
            db.session.close()

def get_product_dao(db=db):
    return ProductDAO(db)