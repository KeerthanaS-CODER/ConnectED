from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session handling

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
programs_collection = db[COLLECTION_NAME]

# Home page where mentor submits program details
@app.route('/mentor', methods=['GET', 'POST'])
def mentor_form():
    if request.method == 'POST':
        program_data = {
            'program_name': request.form['program_name'],
            'category':request.form['category'],
            'duration': request.form['duration'],
            'available_slots': request.form['available_slots'],
            'overview': request.form['overview'],
            'learning_path': request.form['learning_path'],
            'highlights': request.form['highlights'],
            'preliminary_domains': request.form['preliminary_domains'],
            'supplemented_domains': request.form['supplemented_domains'],
            'requirements': request.form['requirements'],
            'deadline': request.form['deadline']
        }
        programs_collection.insert_one(program_data)
        
        # Flash a success message
        flash('Program has been successfully added!', 'success')
        
        return redirect('/programs')
    
    return render_template('form.html')

# Mentee page where they view the list of programs
@app.route('/programs', methods=['GET'])
def view_programs():
    programs = list(programs_collection.find())
    return render_template('programs.html', programs=programs)

if __name__ == '__main__':
    app.run(port=5002)
