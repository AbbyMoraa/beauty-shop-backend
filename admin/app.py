from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from routes.admin_routes import admin_bp

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'test-secret-key-dont-use-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

jwt = JWTManager(app)

app.register_blueprint(admin_bp)

@app.route('/')
def home():
    return {
        'message': 'Beauty Shop Admin API Test Server',
        'endpoints': {
            'login': '/login (POST)',
            'orders': '/api/admin/orders (GET)',
            'analytics': '/api/admin/analytics/products (GET)',
            'users': '/api/admin/users (GET)',
            'export': '/api/admin/export/orders (GET)'
        },
        'note': 'All admin endpoints need JWT token except /login'
    }

@app.route('/login', methods=['POST'])
def login():
    token = create_access_token(identity='test_admin')
    return {
        'access_token': token,
        'message': 'Use this token in Authorization header: Bearer <token>'
    }

if __name__ == '__main__':
    print("Starting admin test server...")
    print("Go to http://localhost:5000 to see available endpoints")
    print("First visit /login to get a JWT token")
    app.run(debug=True, port=5000)