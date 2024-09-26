# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    with app.app_context():
        # Importando as rotas
        from .views import main as main_blueprint
        app.register_blueprint(main_blueprint)

    return app
