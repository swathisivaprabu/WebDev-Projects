from flask import Flask, request, render_template, jsonify
import mysql.connector
#importing libs
app = Flask(__name__)

# Database connection and cursor 
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2005",
    database="stu_reg"
)

cursor = db.cursor()

# Route to display the HTML form
@app.route('/')
def registration_form():
    return render_template('notepadex1.html')

# Route to handle form submission
@app.route('/notepadex1', methods=['POST'])
def register():
    try:
        # Fetch form data
        name = request.form['name']
        age=request.form['age']
        gender = request.form['gender']
        dob = request.form['dob']
        email = request.form['email']

        cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result:
            return '''
            <h1>"Email already exists! Please use a different email."</h1>
            <a href="/">Go back to the form </a> '''
        else:

        # Insert data into the database
            cursor.execute(
                 "INSERT INTO students (name, age, gender, dob, email) VALUES (%s, %s, %s, %s, %s)",
                 (name, age, gender, dob, email)
                )
            db.commit()

        # Return success message after insertion
            return "Registration successful!"

    except mysql.connector.Error as err:
        return f"Error: {err}"


#to get all the value from the database from the table
'''@app.route('/api/students',methods=['GET'])
def api_get_students():
    cursor.execute("SELECT * FROM students")
    students=cursor.fetchall()
    #conversion into list of dictionaries

    student_list=[]
    for student in students:
        student_list.append({
            "id":student[0],
            "name":student[1],
            "age":student[2],
            "gender":student[3],
            "dob":student[4],
            "email":student[5]
            })
    return jsonify(student_list)'''

#to just get one
@app.route('/get_student',methods=['GET','POST'])
def get_student():
    stu_id=request.args.get('id')
    cursor.execute("SELECT * FROM students WHERE id= %s",(stu_id,))
    result=cursor.fetchone()

    if result:

        student={
            "id":result[0],
            "name":result[1],
            "age":result[2],
            "gender":result[3],
            "dob":result[4],
            "email":result[5]
            }
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found!"}),404


@app.route('/check_email',methods=['POST'])
def check_email():
    cursor.execute("SELECT * FROM students WHERE email=%s", (email,))
    result=cursor.fetchone()

    if result:
        return jsonify({"status":"exists","meassage": "Email already exist!"}),400
    else:
        return jsonify({"status":"available","message":"Email is availabe!"}),200
    


if __name__ == '__main__':
    app.run(debug=True)
    

    
