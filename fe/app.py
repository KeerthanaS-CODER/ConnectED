from flask import Flask, request, redirect, url_for, flash, send_from_directory, session
from pymongo import MongoClient
import random
import smtplib
from email.message import EmailMessage
import gridfs

app = Flask(__name__)
app.secret_key = '587'  

otp_generated = None
user_data = {}  

client = MongoClient('mongodb+srv://keerthikms1047:r.8y9ZAAG2ts%40hx@cluster0.3xiqy.mongodb.net/')
db = client['resume_db']
fs = gridfs.GridFS(db)

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_otp_via_email(otp, user_email):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    from_email = "shreyasaditya04@gmail.com"
    password_mail = 'fbzq sskn vvqy swbg' 
    server.login(from_email, password_mail)
    msg = EmailMessage()
    msg['Subject'] = 'Your OTP Code'
    msg['From'] = from_email
    msg['To'] = user_email
    msg.set_content(f'Your OTP is: {otp}')
    server.send_message(msg)
    server.quit()

# Serve the landing page (entry.html)
@app.route('/')
def entry():
    return send_from_directory('pages', 'entry.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    global otp_generated
    email = request.form.get('email')
    password = request.form.get('password')  

    if email:
        otp_generated = generate_otp()
        send_otp_via_email(otp_generated, email)
        
        user_data[email] = password
        flash('OTP sent to your email. Please check and enter it below.')
        return redirect(url_for('verify'))
    else:
        flash('Please enter a valid email address.')
        return redirect(url_for('signup'))

# Serve the signup page (Signup.html)
@app.route('/signup')
def signup():
    return send_from_directory('pages', 'Signup.html')

@app.route('/verify')
def verify():
    return send_from_directory('pages', 'VerifyEmail.html')

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    global otp_generated
    entered_otp = request.form.get('otp')
    
    if entered_otp == otp_generated:
        flash('OTP verified successfully! You can now login.')
        return redirect(url_for('login'))
    else:
        flash('Invalid OTP. Please try again.')
        return redirect(url_for('verify'))

@app.route('/login')
def login():
    return send_from_directory('pages', 'Login.html')

@app.route('/login_user', methods=['POST'])
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email in user_data and user_data[email] == password:
        flash('Login successful!')
        return redirect(url_for('booking'))
    else:
        flash('Invalid email or password. Please try again.')
        return redirect(url_for('login'))

@app.route('/booking')
def booking():
    return send_from_directory('pages', 'Booking.html')

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        flash('No file part')
        return redirect(url_for('booking'))

    file = request.files['resume']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('booking'))

    if file:
        filename = file.filename
        file_id = fs.put(file, filename=filename)
        flash(f'Resume uploaded successfully: {filename}')
        return redirect(url_for('booking'))

@app.route('/pages/<path:filename>')
def serve_page(filename):
    try:
        return send_from_directory('pages', filename)
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
