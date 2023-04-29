from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
from flask import app, render_template
import requests
@app.route('/send_otp', methods=['POST'])
def send_otp():
    # Get the mobile number and email address entered by the user
    mobile_number = requests.form['mobile_number']
    email = requests.form['email']
    
    # Generate a 6-digit OTP
    otp = str(random.randint(100000, 999999))
    
    # Separate the first 3 digits and the last 3 digits of the OTP
    otp_mobile = otp[:3]
    otp_email = otp[3:]
    
    # Send the first 3 digits of the OTP to the mobile number via SMS message using TextMagic API
    api_key = 'your_textmagic_api_key'
    
    response = requests.post('https://rest.textmagic.com/api/v2/messages',
        auth=('api', api_key),
        data={
            'text': 'Your OTP is ' + otp_mobile,
            'phones': mobile_number
        }
    )
    
    # Send the last 3 digits of the OTP to the email address
    sender_email = 'your_sender_email_address'
    sender_password = 'your_sender_email_password'
    recipient_email = email
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'OTP for validation'
    
    msg.attach(MIMEText('Your OTP is ' + otp_email, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)
    server.quit()
    
    # Render a new HTML page to ask the user to enter the OTP
    return render_template('verify.html', mobile_number=mobile_number, email=email)
