from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from PyPDF2 import PdfReader
import os

app = Flask(__name__)
CORS(app)  # This will allow all origins by default

# Connect to MongoDB
client = MongoClient("mongodb+srv://keerthikms1047:r.8y9ZAAG2ts%40hx@cluster0.3xiqy.mongodb.net/")
db = client["patent_db"]
projects = db["projects"]

# Folder for uploaded files
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return 'Welcome to the Patent Flow Application!'

# Route for file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    reader = PdfReader(file_path)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()

    matched = False
    for project in projects.find():
        title = project.get('title', "").lower()
        keywords = [kw.lower() for kw in project.get('keywords', [])]

        if any(word in pdf_text.lower() for word in [title] + keywords):
            matched = True
            break

    response_message = 'Continue the patent flow' if matched else 'Patent flow cannot proceed'
    print(response_message)  # Print the response message for debugging

    return jsonify({'message': response_message}), 200 if matched else 400

if __name__ == '__main__':
    app.run(port=5003,debug=True)