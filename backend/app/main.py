from src.app import configure_app
from src.app import socketio
from src.blueprints.inspection import inspection
from src.blueprints.scan import scan
from src.blueprints.test import test

app = configure_app()
app.register_blueprint(test, url_prefix="/api/test")
app.register_blueprint(inspection, url_prefix="/api/inspection")

if __name__ == '__main__':
    socketio.run(app)
