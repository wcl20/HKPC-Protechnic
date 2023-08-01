from .config import configs
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

socketio = SocketIO()

def configure_app(stage="development"):
    app = Flask(__name__, static_folder='../static', static_url_path="/api/static")
    app.config.from_object(configs[stage])
    # Allow Cross Origin Resource Sharing (CORS)
    CORS().init_app(app)
    # Socket IO
    socketio.init_app(app, cors_allowed_origins="*")
    return app

@socketio.on("connect")
def socket_connect():
    print("Socket Connected")
