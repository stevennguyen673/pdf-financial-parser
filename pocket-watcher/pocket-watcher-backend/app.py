from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
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
    file_path = os.path.join(app.static_folder, path)
    if path != "" and os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
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

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/generate_goal', methods=['POST'])
def generate_goal():
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
    file = request.files.get('file')
    if not file or file.filename == '':
        return jsonify({'error': 'No PDF uploaded'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        result = parse_pdf(filepath)

        total_spending = sum(child["value"] for child in result["circle_packing_data"]["children"])

        return jsonify({
            "success": True,
            "chartUrls": {
                "pie": result["chart_url"]
            },
            "totalSpending": total_spending,
            "circle_data": result["circle_packing_data"],
            "sankey_data": result["sankey_data"]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
