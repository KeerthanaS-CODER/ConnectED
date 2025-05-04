from flask import Flask, request, render_template
import os
import docx2txt
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
import gridfs
from bson import ObjectId

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['resume_db']
fs = gridfs.GridFS(db)

# Existing functions...

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""

def extract_text_from_file(file_id):
    file = fs.get(file_id)
    file_type = file.filename.split('.')[-1]
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    
    with open(file_path, 'wb') as f:
        f.write(file.read())

    if file_type == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_type == 'docx':
        return extract_text_from_docx(file_path)
    elif file_type == 'txt':
        return extract_text_from_txt(file_path)
    return ""

@app.route("/")
def matchresume():
    return render_template('matchresume.html')

@app.route('/matcher', methods=['POST'])
def matcher():
    if request.method == 'POST':
        job_description = request.form['job_description']
        resume_files = request.files.getlist('resumes')

        # Handle resume uploads
        resume_ids = []
        resumes = []
        resume_filenames = []

        for resume_file in resume_files:
            filename = resume_file.filename
            file_id = fs.put(resume_file, filename=filename)
            resume_ids.append(file_id)
            text = extract_text_from_file(file_id)
            resumes.append(text)
            resume_filenames.append(filename)

        if not resumes or not job_description:
            return render_template('matchresume.html', message="Please upload resumes and enter a job description.")

        # Vectorize job description and resumes
        vectorizer = TfidfVectorizer().fit_transform([job_description] + resumes)
        vectors = vectorizer.toarray()

        # Calculate cosine similarities
        job_vector = vectors[0]
        resume_vectors = vectors[1:]
        similarities = cosine_similarity([job_vector], resume_vectors)[0]

        # Get top 20 resumes and their similarity scores
        top_indices = similarities.argsort()[-20:][::-1]
        top_resumes = [resume_filenames[i] for i in top_indices]
        similarity_scores = [round(similarities[i] * 100, 2) for i in top_indices]  # Convert to percentage

        return render_template('matchresume.html', message="Top matching resumes:", top_resumes=top_resumes, similarity_scores=similarity_scores)

    return render_template('matchresume.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
