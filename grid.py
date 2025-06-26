from flask import Flask, request, render_template, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2005",
    database="stu_reg"
)
cursor = db.cursor()

@app.route ('/')
def index():
    return render_template('grid.html')

@app.route('/view_table', methods=['GET', 'POST'])
def view_table():
    if request.method == 'POST':
        table_name = request.form.get('table_name')
        search_email = request.form.get('search_email')
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            if search_email:
                cursor.execute(f"SELECT * FROM {table_name} WHERE email='{search_email}'")
                rows = cursor.fetchall()
            if not rows:
                return render_template('grid.html', error="No data found in the table or no matching email.")
            return render_template('grid.html', data=rows)
        except mysql.connector.Error as err:
            return render_template('grid.html', error=f"Error: {err}")
    
    return render_template('grid.html')

if __name__ == '__main__':
    app.run(debug=True)