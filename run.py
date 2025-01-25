from quart import Quart
from quart_cors import cors
from app.routes.analysis import analysis_bp
from app.config import config

def create_app():
    app = Quart(__name__)
    app = cors(app, allow_origin="*")

    # Register blueprint
    app.register_blueprint(analysis_bp)

    # Debug routes
    @app.before_serving
    async def show_routes():
        print("Registered routes:")
        for rule in app.url_map.iter_rules():
            print(f"- {rule}")

    return app

# Create app instance for ASGI servers
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)