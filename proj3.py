from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from flask_mail import Mail, Message

app = Flask(__name__)

# Flask Mail 
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''#removed for privacy 
app.config['MAIL_PASSWORD'] = ''#can be generated through account password 
app.config['MAIL_DEFAULT_SENDER'] = ''

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stu_reg"
)

cursor = db.cursor()

mail = Mail(app)

@app.route('/')
def user_name():
    return render_template('pg3.html')


@app.route('/pg3', methods=["POST"])
def login():
    try:
        user_email = request.form['email']
        user_password = request.form['pass']

        cursor.execute("SELECT * FROM username WHERE email = %s", (user_email,))
        result = cursor.fetchone()

        if result:
            stored_pass = result[7]  
            if stored_pass == user_password:  
                return redirect(url_for('registration_form'))  
            else:
                return '''
                    Incorrect password. Please try again.
                    <a href="/">Go Back to Login</a>
                '''
        else:
            return '''
                User do not exist.
                <a href="/">Go Back to Login</a>
            '''
    except mysql.connector.Error as err:
        return f"Error: {err}"

@app.route('/registration_form')
def registration_form():
    return render_template('pg3form.html')  

@app.route('/pg3form', methods=['POST'])
def register():
    try:
        nm = request.form['namef']
        email = request.form['email']
        dept = request.form['dept']
        purpose = request.form['purpose']

        cursor.execute("INSERT INTO webinar (name, email, department, purpose) VALUES (%s,%s,%s,%s)",(nm,email,dept,purpose));

        #Email message
        msg = Message(
         subject="Permission for Webinar Hosting",
         recipients=[""],
         html=f"""
        <html>
        <body>
            <p>A user with the following details has registered:</p>
            <ul>
                <li><strong>Name:</strong>{nm}<li>
                <li><strong>Email:</strong> {email}</li>
                <li><strong>Department:</strong> {dept}</li>
                <li><strong>Purpose:</strong> {purpose}</li>
            </ul>
            <p>Select Any one:</p>
            <a href="{url_for('approve_registration', _external=True, student_email=email, action='yes', user_name=nm)}"
               style="display: inline-block; padding: 10px 20px; color: white; background-color: green; text-decoration: none; border-radius: 5px; font-weight: bold;">
               Approve
            </a>
            <a href="{url_for('approve_registration', _external=True, student_email=email, action='no', user_name=nm)}"
               style="display: inline-block; padding: 10px 20px; color: white; background-color: red; text-decoration: none; border-radius: 5px; font-weight: bold;">
               Decline
             </a>
           </body>
           </html>
            """
           )
        mail.send(msg)
        return '''<center><h3>Submission is successful! Wait for the reply </h3></center>'''

    except mysql.connector.Error as err:
        return f"Error: {err}"

@app.route('/approve_registration')
def approve_registration():
    student_email = request.args.get('student_email')
    action = request.args.get('action')

    if action == 'yes':
        cursor.execute("UPDATE webinar SET registration_status = 'approved' WHERE email = %s", (student_email,))
        db.commit()
        #Acceptance Email
        msg = Message(
            subject="Your Registration has been accepted",
            recipients=[student_email],
            body="Your registration has been accepted.Thank You!"
        )
        mail.send(msg)
        
        return "Student registration approved."
    elif action == 'no':
        cursor.execute("UPDATE webinar SET registration_status = 'declined' WHERE email = %s", (student_email,))
        db.commit()
        #Decline Email
        msg = Message(
            subject="Your Registration is Declined",
            recipients=[student_email],
            body="We're sorry, your registration has been declined.Thank You!"
        )
        mail.send(msg)

        return "Student registration declined."
    else:
        return "Invalid action."


if __name__ == '__main__':
    app.run(debug=True)
