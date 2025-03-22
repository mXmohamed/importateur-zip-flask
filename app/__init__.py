from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import datetime

# Initialisation de l'extension
db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    """Fonction factory pour créer l'application Flask."""
    app = Flask(__name__)
    
    # Configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_key_change_in_production'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    # Si une configuration spécifique est fournie, on l'applique
    if config:
        app.config.from_mapping(config)
    
    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Enregistrement des blueprints
    from app.routes.imports import imports_bp
    app.register_blueprint(imports_bp, url_prefix='/')
    
    # Contexte global pour les templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
    
    return app