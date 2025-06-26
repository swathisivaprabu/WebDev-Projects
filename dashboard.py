from flask import Flask, request, render_template, jsonify, session, redirect, url_for
import mysql.connector
from datetime import datetime
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web
from matplotlib import pyplot as plt
import seaborn as sns
import io
import base64

file_path = r'C:\Users\Sabari\Desktop\Swathi-cllg\web_dev_projects\web_dev_projects\templates\ldap_registered_users.csv'   #links in python should start with r to be recognized 

app = Flask(__name__)
app.secret_key = 'Kj8N2m9P5q1R7s3T6u0V4w8X2y5Z9a1B3c7D4e6F8g2H5i9J0k3L7m1N4o8P2q6' #or any secret key wnated 

# Database configuration - Your way
db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="", #password
    database="stu_reg"
)
cursor = db.cursor()

# Load DataFrame globally
df = pd.read_csv(file_path)

def create_plots():
    """Create plots and return them as base64 encoded images for web display"""
    
    # Plot 1: Department-wise Count
    plt.figure(figsize=(10, 8))
    department_counts = df['Department'].value_counts()
    counts = department_counts.sort_values()
    ax = counts.plot(kind='barh', figsize=(10, 8), color=sns.color_palette('Dark2'))

    # Add value labels
    for i, v in enumerate(counts):
        ax.text(v + 2, i, str(v), color='black', va='center')

    plt.xlabel("Count")
    plt.ylabel("Department")
    plt.title("Department-wise Count")
    plt.grid(axis='x', linestyle='--', alpha=0.5)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    
    # Convert plot to base64 for web display
    img1 = io.BytesIO()
    plt.savefig(img1, format='png', bbox_inches='tight')
    img1.seek(0)
    plot1_url = base64.b64encode(img1.getvalue()).decode()
    plt.close()

    # Plot 2: Activation Status
    count_activate = 0
    not_activate = 0

    # Iterate through the 'activation' column
    for value in df['activation']:
        # Check if the value is NaN (not activated)
        if pd.isna(value):
            count_activate += 1  # Fixed: NaN not a number in this case null 
        else:
            not_activate += 1

    print(f"Number of activated users: {count_activate}")
    print(f"Number of non-activated users: {not_activate}")

    # Create a bar chart to visualize the activation status
    status_counts = [count_activate, not_activate]
    labels = ['Activated', 'Non-Activated']

    plt.figure(figsize=(8, 6))
    plt.bar(labels, status_counts, color=['green', 'red'])
    plt.xlabel('Activation Status')
    plt.ylabel('Count')
    plt.title('Activation Status Count')
    plt.tight_layout()
    
    # Convert plot to base64 for web display
    img2 = io.BytesIO()
    plt.savefig(img2, format='png', bbox_inches='tight')
    img2.seek(0)
    plot2_url = base64.b64encode(img2.getvalue()).decode()
    plt.close()

    # Return both images as base64 strings
    return {
        'department_plot': plot1_url,
        'activation_plot': plot2_url,
        'activated_count': count_activate,
        'not_activated_count': not_activate
    }

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            # Using your MySQL connection approach
            cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            
            if user:
                session['admin_logged_in'] = True
                session['admin_username'] = username
                session['user'] = username  # Added for consistency
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error="Invalid username or password")
                
        except mysql.connector.Error as err:
            return render_template('login.html', error=f"Database Error: {err}")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login_page'))  # Fixed function name
    
    try:
        # Get basic stats from DataFrame
        stats = {
            'total_employees': len(df),
            'total_departments': df['Department'].nunique(),
            'designations': df['Designation'].nunique() if 'Designation' in df.columns else 0
        }
        return render_template('dashboard.html', username=session['user'], stats=stats)
    except Exception as e:
        return render_template('dashboard.html', username=session['user'], error=str(e))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user' not in session:
        return redirect(url_for('login_page'))  # Fixed function name
    
    employee = None
    message = None
    
    if request.method == 'POST':
        emp_id = request.form['employee_id']
        try:
            employee_row = df[df['Employee_No'] == emp_id]
            if not employee_row.empty:
                employee = employee_row.iloc[0].to_dict()
            else:
                message = f"No employee found with ID: {emp_id}"
        except ValueError:
           message = "Please enter a valid Employee ID (number)"
        except Exception as e:
            message = f"Error: {str(e)}"
    
    return render_template('search.html', employee=employee, message=message)

@app.route('/analytics')
def analytics():
    if 'user' not in session:
        return redirect(url_for('login_page'))  # Fixed function name
    
    try:
        plots_data = create_plots()  # Get the plot data
        
        # Get some statistics
        stats = {
            'total_employees': len(df),
            'total_departments': df['Department'].nunique(),
            'designations': df['Designation'].nunique() if 'Designation' in df.columns else 0
        }
        
        return render_template('analytics.html', plots=plots_data, stats=stats)
    except Exception as e:
        return render_template('analytics.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
