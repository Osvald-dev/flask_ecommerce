from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import g, current_app
from flask_api.db import db
from flask_api.user.user_model import User

class UsuarioDAO:

    def __init__(self, db):
        self.db = db
        self.session = db.session

    def close_session(self, exception=None):
        session = getattr(g, '_session', None)
        if session is not None:
            session.close()

    def create(self, username,email,password,is_admin):
        try:
            existing_user = self.session.query(User).filter_by(email=email).first()
            if existing_user:
                raise ValueError("El correo electrónico ya está en uso")
            
            usuario = User(username=username, email=email, password=password, is_admin=is_admin)
            usuario.set_password(password)
            self.session.add(usuario)
            self.session.commit()
            return usuario
        except IntegrityError as e:
            self.session.rollback()
            if "username" in e.orig.diag.constraint_name:
                raise ValueError("El nombre de usuario ya está en uso")
            elif "email" in e.orig.diag.constraint_name:
                raise ValueError("El correo electrónico ya está en uso")
            else:
                raise e
              
    def get_id(self, id):
        try:
            usuario = self.session.query(User).filter_by(id=id).first()
            return usuario
        except SQLAlchemyError as e:
            raise e
        
    def get_by_email(self, email):
        try:
            usuario = self.session.query(User).filter_by(email=email).first()
            return usuario
        except SQLAlchemyError as e:
            raise e
        
    def update(self, id, username=None, email=None, password=None):
        try:
            usuario = self.get_id(id)
            if usuario:
                if username:
                    usuario.username = username
                if email:
                    usuario.email = email
                if password:
                    usuario.set_password(password)
                self.session.commit()
                return usuario
            else:
                return None
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    def username_exist(self,username):
        try:
            usuario = self.session.query(User).filter_by(username=username).first()
            return usuario
        except SQLAlchemyError as e:
            raise e

    def delete_id(self, id):
        try:
            usuario = self.get_id(id)
            if usuario:
                self.session.delete(usuario)
                self.session.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def list(self):
        try:
            usuarios = self.session.query(User).all()
            # lista serializada
            return [usuario.serialize() for usuario in usuarios]
        except SQLAlchemyError as e:
            raise e
        
    def shutdown_session(exception=None):
        db = getattr(g, '_database', None)
        if db is not None:
            db.session.close()