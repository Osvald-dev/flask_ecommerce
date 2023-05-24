
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_api.db import db



class Product(db.Model):
    __tablename__="product"

    id=db.Column(Integer, primary_key=True, autoincrement=True)
    name=db.Column(String(100), nullable=False)
    price=db.Column(Integer, nullable=False)
    description= db.Column(String(255))
    quantity=db.Column(Integer, nullable=False, default=0)
    cart_id= db.Column(Integer, ForeignKey('cart.id'))
    cart = relationship('Cart', back_populates='product')

    def __init__(self, product, price, description=None, quantity=0):
        self.product = product
        self.price = price
        self.description = description
        self.quantity = quantity

    def serialize(self):
        return {
            'id': self.id,
            'product': self.product,
            'price': self.price,
            'description': self.description,
            'quantity': self.quantity
        }
