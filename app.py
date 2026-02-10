from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from admin.routes.admin_routes import admin_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-this'
CORS(app)
jwt = JWTManager(app)
app.register_blueprint(admin_bp)

@app.route('/')
def home():
    return 'Beauty Shop Admin API Running'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
