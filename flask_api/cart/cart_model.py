
from sqlalchemy import Column, String, Integer, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship
from flask_api.db import db

metadata = db.metadata

cart_products = Table('cart_products',
                       metadata,                      
                       db.Column('cart_id', Integer, ForeignKey('cart.id')),
                       db.Column('product_id', Integer, ForeignKey('product.id'))
                    )

class Cart(db.Model):
    __tablename__="cart"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer, ForeignKey('user.id'))
    user = db.relationship('User', back_populates='cart')
    product = db.relationship('Product', secondary=cart_products, back_populates='cart')
