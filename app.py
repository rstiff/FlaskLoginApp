from flask import Flask, render_template, flash, redirect, url_for, request, session
import mysql.connector


app = Flask(__name__)

# Secret key
app.secret_key = 'thisisasecret'

# Database connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="thsrocks",
    database="login"
)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = con.cursor()
        # Execute the query
        query = "SELECT * FROM people WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        
        # Fetch the result
        user = cursor.fetchone()
        cursor.close()
        
        # Authentication
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            # Authentication failed
            flash('Invalid username or password', 'error')
            
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = con.cursor()
        
        # Execute query to see if username exists
        query_check = 'SELECT * FROM people WHERE username = %s'
        cursor.execute(query_check, (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash("Username already exists", 'error')
        else:
            # Insert the new user
            query_insert = 'INSERT INTO people (username, password) VALUES (%s, %s)'
            cursor.execute(query_insert, (username, password))
            con.commit()
            flash('Signup successful!', 'success')
            return redirect(url_for('login'))
        
        cursor.close()
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('signup'))

if __name__ == "__main__":
    app.run(debug=True)
