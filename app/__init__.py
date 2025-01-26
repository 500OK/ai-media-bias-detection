from quart import Quart

def create_app():
    app = Quart(__name__)
    
    # Import and register blueprints after app creation
    from app.routes.analysis import analysis_bp
    app.register_blueprint(analysis_bp)
    
    return app
