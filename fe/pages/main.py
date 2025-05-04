from flask_cors import CORS
from flask import Flask, send_file, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import os
import docx2txt
import PyPDF2
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'Uploads/'
CORS(app)
# Ensure the uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Store results globally
parsed_result = {"message": "🔍 Waiting for scheduled time...", "top_resumes": [], "similarity_scores": []}

def extract_text(file_path):
    """Extracts text from different file types."""
    text = ""
    try:
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text
        elif file_path.endswith('.docx'):
            text = docx2txt.process(file_path)
        elif file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
    return text[:5000]  # Limit text for faster processing

def parse_resumes(job_description):
    """Runs resume parsing at the scheduled time and updates results for HTML display."""
    global parsed_result

    resume_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith(('.pdf', '.docx', '.txt'))]

    if not resume_files:
        parsed_result["message"] = "❌ No resumes found in the uploads folder."
        return

    resumes = [extract_text(os.path.join(app.config['UPLOAD_FOLDER'], file)) for file in resume_files]

    if not resumes or all(not resume for resume in resumes):
        parsed_result["message"] = "❌ No readable text extracted from resumes."
        return

    # Apply TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([job_description] + resumes).toarray()

    job_vector = vectors[0]
    resume_vectors = vectors[1:]
    similarities = cosine_similarity([job_vector], resume_vectors)[0]

    top_indices = similarities.argsort()[-3:][::-1]  # Get top 3 matches
    top_resumes = [resume_files[i] for i in top_indices]
    similarity_scores = [round(similarities[i] * 100, 2) for i in top_indices]  # Convert to %

    parsed_result["message"] = f"✅ Resumes processed at {datetime.datetime.now().strftime('%H:%M:%S')}"
    parsed_result["top_resumes"] = top_resumes
    parsed_result["similarity_scores"] = similarity_scores

    print(f"Job executed at {datetime.datetime.now()}")  # Log when job runs

@app.route("/")
def index():
    """Serve the main page from the project root."""
    return send_file("index.html")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    """Handles the mentee's resume upload with additional form data."""
    if request.method == "POST":
        file = request.files.get('resume_file')
        name = request.form.get('name')
        email = request.form.get('email')

        if not file:
            return jsonify({"error": "No file uploaded!"}), 400
        if not name or not email:
            return jsonify({"error": "Name and email are required!"}), 400

        # Validate file extension
        if not file.filename.endswith(('.pdf', '.docx', '.txt')):
            return jsonify({"error": "Invalid file type! Only PDF, DOCX, and TXT are allowed."}), 400

        # Save the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Optionally, log or store name and email
        print(f"Received: Name={name}, Email={email}, File={file.filename}")

        return jsonify({"message": f"Resume {file.filename} uploaded successfully for {name}!"})
    return send_file("upload.html")

@app.route("/schedule_resume_parsing", methods=["POST"])
def schedule_resume_parsing():
    """Schedules resume parsing at user-specified time."""
    global parsed_result
    parsed_result = {"message": "🔍 Waiting for scheduled time...", "top_resumes": [], "similarity_scores": []}

    try:
        job_description = request.form.get("job_description")
        schedule_time = request.form.get("schedule_time")

        if not job_description or not schedule_time:
            return jsonify({"error": "Both fields are required!"}), 400

        # Parse schedule time
        schedule_hour, schedule_minute = map(int, schedule_time.split(":"))
        now = datetime.datetime.now()
        run_time = now.replace(hour=schedule_hour, minute=schedule_minute, second=0, microsecond=0)

        if run_time <= now:
            run_time += datetime.timedelta(days=1)  # Schedule for the next day if time has passed

        # Log the schedule time
        print(f"Resume parsing scheduled for {run_time}")

        # Schedule job
        scheduler.add_job(parse_resumes, DateTrigger(run_date=run_time), args=[job_description], id="resume_parser", replace_existing=True)

        parsed_result["message"] = f"⏳ Resume parsing scheduled for {run_time.strftime('%Y-%m-%d %H:%M:%S')}..."
        return send_file("matchresume.html")
    except ValueError:
        return jsonify({"error": "Invalid time format. Use HH:MM format!"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/matchresume")
def match_resume():
    """Display job description and resume matching results."""
    return send_file("matchresume.html")

@app.route("/get_results", methods=["GET"])
def get_results():
    """Return the current parsed results as JSON."""
    return jsonify(parsed_result)

if __name__ == "__main__":
    app.run(debug=True, port=5110)