import random
import smtplib
from email.message import EmailMessage

def generate_otp():
    otp = ''.join([str(random.randint(0, 9)) for i in range(6)])
    return otp

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
    print(f"OTP has been sent to {user_email}")

def get_user_otp():
    return input("Enter the OTP you received: ")

def verify_otp(input_otp, actual_otp):
    if input_otp == actual_otp:
        print("OTP verified")
    else:
        print("Invalid OTP")
    return input_otp == actual_otp

def main():
    to_mail = input("Enter your email address: ")
    otp = generate_otp()
    send_otp_via_email(otp, to_mail)
    attempts = 3
    while attempts > 0:
        user_otp = get_user_otp()
        if verify_otp(user_otp, otp):
            print("Access granted")
            return
        else:
            attempts -= 1
            print(f"Incorrect OTP. You have {attempts} attempts left.")
    print('Access denied!')

main()
