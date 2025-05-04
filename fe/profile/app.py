from flask import Flask, render_template, request, redirect, send_file
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import base64
from io import BytesIO

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb+srv://keerthikms1047:r.8y9ZAAG2ts%40hx@cluster0.3xiqy.mongodb.net/")
db = client['profile']
profile_collection = db['project']

@app.route('/')
def index():
    return render_template('profile.html')

@app.route('/submit-profile', methods=['POST'])
def submit_profile():
    profile_data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "bio": request.form['bio'],
        "skills": request.form['skills'],
        "experience": request.form['experience']
    }

    if 'profile_image' in request.files:
        image_file = request.files['profile_image']
        if image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            profile_data['profile_image'] = image_data

    profile_collection.update_one(
        {"email": profile_data['email']}, 
        {"$set": profile_data}, 
        upsert=True
    )
    return redirect('/profile')

@app.route('/profile')
def profile():
    profile = profile_collection.find_one()
    return render_template('view_profile.html', profile=profile)

@app.route('/edit-profile')
def edit_profile():
    profile = profile_collection.find_one()
    return render_template('edit_profile.html', profile=profile)

@app.route('/update-profile', methods=['POST'])
def update_profile():
    profile_data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "bio": request.form['bio'],
        "skills": request.form['skills'],
        "experience": request.form['experience']
    }

    if 'profile_image' in request.files:
        image_file = request.files['profile_image']
        if image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            profile_data['profile_image'] = image_data

    profile_collection.update_one(
        {"email": profile_data['email']}, 
        {"$set": profile_data}
    )
    return redirect('/profile')

@app.route('/image/<email>')
def get_image(email):
    profile = profile_collection.find_one({"email": email})
    if profile and 'profile_image' in profile:
        image_data = base64.b64decode(profile['profile_image'])
        return send_file(BytesIO(image_data), mimetype='image/jpeg')
    return "No image found"

if __name__ == "__main__":
    app.run(port=5001)
