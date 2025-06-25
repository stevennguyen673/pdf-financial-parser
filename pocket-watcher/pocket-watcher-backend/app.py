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
    data = request.json
    income = float(data.get('income'))
    goal = float(data.get('goal'))
    total_spent = float(data.get('total_spending'))  #passing from front end.

    result = generate_goal_chart(income, goal, total_spent)
    return jsonify(result)

@app.route('/process', methods=['POST'])
def process_data():
    

    chart_urls = {
        "pie": "/static/pie_chart.png",
        "donut": "/static/donut_chart.png",
        "bar": "/static/bar_chart.png",
        "circle": "/static/circle.html",
        "sankey": "/static/sankey.html"
    }

    return jsonify({
        "success": True,
        "chartUrls": chart_urls,
        "totalSpending": total_spending,
        "circle_data": circle_data,
        "sankey_data": sankey_data,
    })



if __name__ == '__main__':
    app.run(debug=True)
