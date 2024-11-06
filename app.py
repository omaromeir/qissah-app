from flask import Flask, send_from_directory, abort
from api.api_routes import api_blueprint  # Import API routes
import os

app = Flask(__name__, static_folder='public')
app.register_blueprint(api_blueprint)  # Register API routes from api/api_routes.py

# Serve the main Svelte app
@app.route('/')
def serve_svelte_app():
    return send_from_directory(app.static_folder, 'index.html')

# Serve static files in the public folder, including the build directory
@app.route('/<path:path>')
def serve_static_files(path):
    full_path = os.path.join(app.static_folder, path)
    if os.path.isfile(full_path):
        return send_from_directory(app.static_folder, path)
    elif os.path.isfile(os.path.join(app.static_folder, 'build', path)):
        return send_from_directory(os.path.join(app.static_folder, 'build'), path)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
