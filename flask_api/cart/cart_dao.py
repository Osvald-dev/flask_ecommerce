from flask import g, current_app
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_api.cart.cart_model import Cart
from flask_api.db import db


class CartDao:
    def __init__(self, db):
        self.db = db
        self.session = db.session

    def close_session(self, exception=None):
        session = getattr(g, '_session', None)
        if session is not None:
            session.close()

    def create_cart(self,user_id):
        cart = Cart(user_id=user_id)
        self.session.add(cart)
        self.session.commit()
        self.session.refresh(cart)
        self.session.close()
        return cart
    
    def get_cart_by_id(self, cart_id):
        cart= self.session.query(Cart).filter(Cart.id == cart_id).first()
        self.session.close()
        return cart
    
    def add_product_to_cart(self, cart_id, product_id):
        cart = self.session.query(Cart).filter(Cart.id == cart_id).first()
        cart.products.append(product_id)
        self.session.commit()
        self.session.close()

    def shutdown_session(exception=None):
        db = getattr(g, '_database', None)
        if db is not None:
            db.session.close()