from flask import Flask, request, render_template, session, redirect, url_for
from flask_mail import Mail, Message
import string
import random
from datetime import timedelta

app = Flask(__name__)

# Configure mail settings (replace with your actual values)
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@domain.com'
app.config['MAIL_PASSWORD'] = 'your-password'

mail = Mail(app)

# List of valid recipient emails
recipent_email = ["abcd"]

# Generate a temporary password
temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

app.secret_key = '2134dfbs345dfdg5'

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=1)

@app.route('/', methods=['POST'])
def login():
    email = request.form.get('email')
    if email in recipent_email:
        # Send the temporary password via email
        msg = Message('Your temporary password', sender='your-email@domain.com', recipients=[email])
        msg.body = f'Your temporary password is {temp_password}'
        mail.send(msg)

        # Store email and temporary password in session
        session['email'] = email
        session['temp_password'] = temp_password
        return render_template('index.html')
        # return redirect(url_for('password')), 200
    else:
        return 'Email does not match', 400

@app.route('/password', methods=['POST'])
def password():
    entered_password = request.form.get('password')
    if entered_password == session.get('temp_password'):
        return redirect(url_for('report')), 200
    else:
        return 'Incorrect password', 400

@app.route('/report', methods=['GET'])
def report():
    if 'email' in session:
        # Render the report (replace with your actual logic)
        return render_template('report.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('temp_password', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5000)
