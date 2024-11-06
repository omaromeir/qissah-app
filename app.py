from flask import Flask, render_template, send_from_directory, abort
from api.api_routes import api_blueprint  # Import API routes
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api_blueprint)  # Register API routes from api/api_routes.py

# Serve the main Alpine.js app (index.html) from the templates directory
@app.route('/')
def serve_index():
    return render_template('index.html')

# Serve static files (e.g., JavaScript or images) directly from a specified directory
@app.route('/static/<path:filename>')
def serve_static_files(filename):
    static_folder_path = os.path.join(app.root_path, 'static')
    if os.path.isfile(os.path.join(static_folder_path, filename)):
        return send_from_directory(static_folder_path, filename)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)