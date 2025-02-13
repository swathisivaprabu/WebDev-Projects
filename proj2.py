from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''  #email id 
app.config['MAIL_PASSWORD'] = ''        # use the app password from google accounts so u can acess the mail to send mail to the default sender
app.config['MAIL_DEFAULT_SENDER'] = '' 

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",#password
    database="stu_reg"
)

cursor = db.cursor()

mail = Mail(app)

@app.route('/')
def login_form():
    return render_template('pg2.html')


@app.route('/pg2', methods=['POST'])
def login():
    try:
        user = request.form['userid']
        passw = request.form['pass']

        cursor.execute("SELECT pass FROM username WHERE user = %s", (user,))
        result = cursor.fetchone()

        if result:
            stored_pass = result[0]
            if stored_pass == passw:
                return redirect(url_for('student_dashboard'))
            else:
                return '''
                    The given password is wrong. Try Again...
                    <a href="/">Go back to login</a>'''
        else:
            return '''
                <h5>User ID does not exist. Create one.</h5>
                <a href="/pg2reg.html">Registration Form</a>'''

    except mysql.connector.Error as err:
        return f"Error: {err}"


@app.route('/pg2reg.html')
def registration_form():
    return render_template('pg2reg.html')


@app.route('/pg2reg', methods=['GET', 'POST'])
def register():
    try:
        nmf = request.form['namef']
        nml = request.form['namel']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        dept = request.form['dept']
        preuser = request.form['prefuser']

        cursor.execute("SELECT * FROM username WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result:
            return '''
            <h1>Email already exists! Please use a different email.</h1>
            <a href="/">Go back to the form</a>'''
        else:
            cursor.execute("INSERT INTO username (namef, namel, gender, dob, email, dept, user, pass) VALUES (%s, %s, %s, %s, %s, %s, %s, NULL)", (nmf, nml, gender, dob, email, dept, preuser))
            db.commit()
            msg = Message(
                subject="New User Registration Details",
                recipients=[""],  # admin email
                body=f"""
            A new user has registered:

            First Name: {nmf}
            Last Name: {nml}
            Date of Birth: {dob}
            Gender: {gender}
            Email: {email}
            Department: {dept}
            Preferred Username: {preuser}

            Admin Dashboard Link: {url_for('admin_dashboard', _external=True)}

            Please create a password for this user and email it to them at {email}.
            """
            )
            mail.send(msg)

            return render_template('success_registration.html')

    except mysql.connector.Error as err:
        return f"Error: {err}"


@app.route('/student_details')
def student_dashboard():
    return "Welcome to the student details page!"


@app.route('/admin_dashboard')
def admin_dashboard():
    try:
        cursor.execute("SELECT namef, namel, dob, gender, email, dept, user FROM username")
        users = cursor.fetchall()  

        return render_template('admin_dashboard.html', users=users)
    except mysql.connector.Error as err:
        return f"Error: {err}"


@app.route('/set_password/<username>', methods=['GET', 'POST'])
def set_password(username):
    if request.method == 'POST':
        password = request.form['password']

        try:
            # Update the password 
            cursor.execute("UPDATE username SET pass = %s WHERE user = %s", (password, username))
            db.commit()

            # Fetch the user's email
            cursor.execute("SELECT email FROM username WHERE user = %s", (username,))
            user_email = cursor.fetchone()[0]

            # Send email to the user with their username and password
            msg = Message(
                subject="Your Login Credentials",
                recipients=[user_email],
                body=f"""
                Hello,

                Your account has been created. Here are your login details:

                Username: {username}
                Password: {password}

                Please log in and update your password immediately for security purposes.

                Regards,
                Admin Team
                """
            )
            mail.send(msg)

            return redirect(url_for('admin_dashboard'))

        except mysql.connector.Error as err:
            return f"Error: {err}"

    return '''
    <h1>Set Password for User</h1>
    <form method="POST">
        <label for="password">Enter Password:</label>
        <input type="password" id="password" name="password" required>
        <button type="submit">Set Password</button>
    </form>
    '''

@app.route('/create_password/<username>', methods=['GET', 'POST'])
def create_password_form(username):
    if request.method == 'POST':
        password = request.form['password']

        try:
            # Update the user's password in the database
            cursor.execute("UPDATE username SET pass = %s WHERE user = %s", (password, username))
            db.commit()

            # Fetch the user's email
            cursor.execute("SELECT email FROM username WHERE user = %s", (username,))
            user_email = cursor.fetchone()[0]

            # Send email to the student with login details
            msg = Message(
                subject="Your Login Credentials",
                recipients=[user_email],
                body=f"""
                Hello,

                Your account has been created. Here are your login details:

                Username: {username}
                Password: {password}

                Please log in and update your password immediately for security purposes.

                Regards,
                Admin Team
                """
            )
            mail.send(msg)

            return redirect(url_for('admin_dashboard'))

        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template('create_password.html', username=username)


if __name__ == '__main__':
    app.run(debug=True)
