import os

from flask import Flask
from routes.main import main_bp
from routes.actions import actions_bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(main_bp)
app.register_blueprint(actions_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
