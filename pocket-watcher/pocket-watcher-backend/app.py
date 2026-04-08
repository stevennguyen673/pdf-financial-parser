from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from utils.parser import parse_pdf
from goals import generate_goal_chart

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
STATIC_FOLDER = 'static'

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path="")
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/<path:path>')
def serve_react(path=''):
    """Serve frontend React app."""
    file_path = os.path.join(app.static_folder, path)
    if path != "" and os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload a PDF and parse it."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            result = parse_pdf(filepath)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Unsupported file type'}), 400


@app.route('/generate_goal', methods=['POST'])
def generate_goal():
    """Generate a savings goal chart based on income, goal, and total spending."""
    data = request.json or {}
    try:
        income = float(data.get('income', 0))
        goal = float(data.get('goal', 0))
        total_spent = float(data.get('total_spending', 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid numeric input"}), 400

    result = generate_goal_chart(income, goal, total_spent)
    return jsonify(result)


@app.route('/process', methods=['POST'])
def process_data():
    """Parse uploaded PDF and return chart URLs and structured data."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Parse PDF
    try:
        result = parse_pdf(filepath)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Load circle and sankey JSON data
    static_dir = os.path.join(os.getcwd(), 'static')
    try:
        with open(os.path.join(static_dir, 'circle_data.json')) as f:
            circle_data = json.load(f)
        with open(os.path.join(static_dir, 'sankey_data.json')) as f:
            sankey_data = json.load(f)
    except Exception:
        circle_data = {}
        sankey_data = {}

    return jsonify({
        "success": True,
        "chartUrls": {
            "pie": result["chart_url"],
            "donut": result["donut_url"],
            "bar3d": result["bar3d_url"]
        },
        "totalSpending": result["totalSpending"],
        "circle_data": circle_data,
        "sankey_data": sankey_data,
    })


@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files."""
    return send_from_directory(app.static_folder, filename)


if __name__ == '__main__':
    app.run(debug=True)
