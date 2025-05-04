from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_pymongo import PyMongo
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# MongoDB connection variables
MONGO_URL = "mongodb+srv://keerthikms1047:r.8y9ZAAG2ts%40hx@cluster0.3xiqy.mongodb.net/recordings?retryWrites=true&w=majority"
DB_NAME = "recordings"
COLLECTION_NAME = "videos"

# Configure MongoDB connection
app.config["MONGO_URI"] = MONGO_URL
mongo = PyMongo(app)

# Test MongoDB connection
try:
    mongo.db.videos.find_one()  # Test a query to the 'videos' collection
    print("Connected to MongoDB successfully.")
except Exception as e:
    print("Failed to connect to the database:", e)

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route to render the frontend
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to get videos
@app.route('/videos', methods=['GET'])
def get_videos():
    try:
        language = request.args.get('language', '')
        domain = request.args.get('domain', '')

        query = {}
        if language:
            query['language'] = language
        if domain:
            query['domain'] = domain

        videos = mongo.db.videos.find(query)
        video_list = []
        for video in videos:
            video_list.append({
                'title': video['title'],
                'url': f"/uploads/{video['filename']}",  # Correct URL for uploaded files
                'language': video['language'],
                'domain': video['domain']
            })

        return jsonify(video_list)
    except Exception as e:
        print("Error getting videos:", e)
        return jsonify({'error': str(e)}), 500

# API endpoint to add a video
@app.route('/videos', methods=['POST'])
def add_video():
    try:
        title = request.form.get('title')
        file = request.files.get('videoFile')  # Use .get() for safer access
        language = request.form.get('language')
        domain = request.form.get('domain')

        if not all([title, file, language, domain]):
            return jsonify({'error': 'Missing data fields'}), 400

        # Save the video file
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Insert the video metadata into the collection
        mongo.db.videos.insert_one({
            'title': title,
            'filename': filename,
            'language': language,
            'domain': domain
        })

        return jsonify({'success': True}), 201
    except Exception as e:
        print("Error adding video:", e)
        return jsonify({'error': str(e)}), 500

# Route to serve uploaded video files
@app.route('/uploads/<path:filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(port=5005, debug=True)
