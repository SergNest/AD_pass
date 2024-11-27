from flask import Flask
from routes.main import main_bp
from routes.actions import actions_bp

app = Flask(__name__)
app.register_blueprint(main_bp)
app.register_blueprint(actions_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
