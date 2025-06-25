Projects
This Folder consists of totally 4 projects primarly focusing on the domain of WEB DEVELOPMENT.

1. HTML Registration Form

	Objective: Create a registration form that collects details such as Name, Email, Date of Birth, Department, Gender, and Purpose of Registration,and stores it in the database,

	Tech Stack Used: HTML, CSS,Python FLASK

	Features:
	 Form validation for input fields.
	 Allows user to submit personal details.

2. Login and Registration System with Flask

	Objective: Implement a login system where users input their email and password, which is validated against stored data in the database.

	Tech Stack Used: Flask, MySQL,HTML,CSS

	Features:
	 Login page with email and password validation.
	 Redirects to a registration form page after a successful login.
	 Password securely stored in the database.
	 Admin receives an email for registration approval after user submits the form.

3. Database Insertion with Flask and MySQL

	Objective: Handle form data submission and insert the user information into a MySQL database.

	Tech Stack Used: Flask, MySQL, Flask-Mail

	Features:
	 Collects user details from the form.
	 Inserts user data into the database.
	 Sends an email to the admin for approval or rejection of the registration.
	 Allows admin to approve or decline registration through email.

4. Email Approval and Rejection System

	Objective: Once a user registers, an email is sent to the admin asking them to approve or reject the registration. The admin can approve or decline directly from the email.
 
	Tech Stack Used: Flask, MySQL, Flask-Mail
 
	Features:
	 Admin can approve or decline registration via a button in the email.
	 The registration status is updated in the database.
	 Sends an email to the user regarding their registration status (approved or declined).
