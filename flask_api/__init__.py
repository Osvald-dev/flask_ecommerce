from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_api.user.user_routes import user_bp
from flask_api.products.product_routes import product_bp
from flask_api.cart.cart_routes import cart_bp
from flask_api.home.routes import home_bp
from flask_api.db import db

jwt_manager = JWTManager()

def create_app(config_file='flask_api.config.Config'):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config_file)
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt_manager.init_app(app)  # Inicializa el JWTManager con tu aplicación Flask
    from flask_api.user.user_model import User
    from flask_api.products.product_model import Product
    from flask_api.cart.cart_model import Cart
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(home_bp)
    return app


# with app.app_context():
#     db.create_all()

# if __name__ == '__main__':
    
#     app.run(debug=True)