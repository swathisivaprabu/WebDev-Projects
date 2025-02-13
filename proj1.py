from flask import Flask, request, render_template, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="",#password 
    database="stu_reg"
)

cursor = db.cursor()

# this route displays the form 
@app.route('/')
def home():
    return render_template('get_student.html')


# takes in the form submission and gives the required output
@app.route('/display_student', methods=['GET', 'POST'])
def display_student():
    stu_id = request.form['id']  # id ->the form
    
    # Query that collects the data from the table
    query = "SELECT * FROM students WHERE id = %s"
    cursor.execute(query, (stu_id,))
    student = cursor.fetchone()

    if student:
        # formating the details to display as in the html form
        details = f"""
        <h1>Student Details</h1>
        <p><strong>ID:</strong> {student[0]}</p>
        <p><strong>Name:</strong> {student[1]}</p>
        <p><strong>Email:</strong> {student[2]}</p>
        <p><strong>Year:</strong> {student[3]}</p>
        <p><strong>Gender:</strong> {student[4]}</p>
        <p><strong>DOB:</strong> {student[5]}</p>
        """
    else:
        #student not found
        details = "<h1>No student found with the given ID!</h1>"

    return details  # Return the html's response 


if __name__ == '__main__':
    app.run(debug=True)




