import bcrypt
from sqlalchemy import Column, String, Integer,Boolean, UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_api.db import db


class User(db.Model):
    __tablename__="user"
    id = db.Column(Integer, autoincrement=True, primary_key=True)
    username= db.Column(String(70), unique=True, nullable=False)
    email = db.Column(String(70), unique=True, nullable=False)
    password = db.Column(String(60), nullable=False)
    is_admin = db.Column(Boolean, default=False, nullable=False)
    cart = db.relationship('Cart', back_populates='user', lazy=True)

    __table_args__=(db.UniqueConstraint('username', name='unique_username'),
                    db.UniqueConstraint('email', name= 'unique_email'))

    def __init__(self, username: str, email: str, password: str, is_admin: Boolean):
        self.username=username
        self.email=email
        self.set_password(password)
        self.is_admin=is_admin

    def set_password(self, password):
        password_bytes = password.encode('utf-8')
        salt= bcrypt.gensalt()
        hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
        self.password = hashed_password_bytes.decode('utf-8')

    def check_password(self, password):
        password_bytes = bytes(password, 'utf-8')
        hashed_password_bytes = self.password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_password_bytes)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'is_admin':self.is_admin
        }

