from flask import Flask, send_from_directory
from api.api_routes import api_blueprint  # Import API routes

app = Flask(__name__, static_folder='public')
app.register_blueprint(api_blueprint)  # Register API routes from api/api_routes.py

# Serve the main Svelte app
@app.route('/')
def serve_svelte_app():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other static files in the Svelte build
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
