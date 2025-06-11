from flask import Flask, render_template, request, session
import sqlite3

app = Flask(__name__)

# Create table (only once)
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS students (name TEXT, email TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return  render_template('index.html')

# ---------- GET Form ----------
@app.route('/loginget')
def login_get():
    return render_template('loginget.html')


@app.route('/loginresult')
def login_result():
    username = request.args.get('username')
    password = request.args.get('password')
    return f"""
        <h3>Received via GET:</h3>
            <h3>hello {username}</h3>
        <a href='/'>Go Home</a>
    """
    
# ---------- POST Form ----------
@app.route('/login', methods=['GET', 'POST'])
def login_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return f"""
            <h3>Received via POST:</h3>
            <h3>hello {username}</h3>
            <a href='/'>Go Home</a>
        """
    return render_template('login.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/view')
def view_records():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    rows = c.fetchall()
    conn.close()

    output = "<h2>Registered Students</h2><ul>"
    for row in rows:
        output += f"<li>Name: {row[0]}, Email: {row[1]}</li>"
    output += "</ul><a href='/'>Go Home</a>"

    return output

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, email) VALUES (?, ?)",
              (name, email))
    conn.commit()
    conn.close()

    return """
        <h3>Data submitted successfully!</h3>
        <a href='/view'>Click here to view all students</a>
    """
    
# ---------- Cookie and session Example ----------

@app.route('/cookie-session')
def cookie_session_form():
    return render_template('cookie_session.html')


@app.route('/set-cookie-session', methods=['POST'])
def set_cookie_and_session():
    name = request.form['name']

    # Set cookie and session
    # make_response is used to create a response object
    resp = make_response(f"""
        <h3>Cookie & Session Set</h3>
        Cookie Value: {name}<br>
        Session Value: {name}<br>
        <a href='/show-cookie-session'>View Stored Values</a><br>
        <a href='/'>Go Home</a>
    """)
    # creating a new cookie
    resp.set_cookie('username', name)

    #creating a new session
    session['user'] = name
    return resp

@app.route('/show-cookie-session')
def show_cookie_and_session():

    # Retrieve cookie and session values if the cookie and session exist with the key 
    #'username' and 'user' or else return 'No cookie set' and 'No session set'
    
    cookie_val = request.cookies.get('username', 'No cookie set')
    session_val = session.get('user', 'No session set')
    return f"""
        <h3>Stored Values</h3>
        Cookie: {cookie_val}<br>
        Session: {session_val}<br>
        <a href='/'>Go Home</a>
    """

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
    
