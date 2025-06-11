# Aim:
# To develop a Flask web application that sets and retrieves session data using HTML forms.

from flask import Flask, session, request, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required to use sessions securely

# HTML template with a form and links to get and clear session data
template = """
<!doctype html>
<title>Session Demo</title>
<h2>Session Example</h2>

<!-- Simple form to accept user's name -->
<form method="POST" action="/setsession">
  Enter your name: <input type="text" name="username">
  <input type="submit" value="Set Session">
</form>
<br>

<!-- Links to check and clear session -->
<a href="/getsession">Check Session</a> <br>
<a href="/clearsession">Clear Session</a>
"""

@app.route('/')
def home():
    # render_template_string is used to embed HTML directly in Python
    return render_template_string(template)

@app.route('/setsession', methods=['POST'])
def setsession():
    username = request.form.get('username')

    # Session data is stored server-side, but a session ID is saved in the user's browser cookie
    session['username'] = username

    return "Session has been set for user: {}<br><a href='/'>Go back</a>".format(username)

@app.route('/getsession')
def getsession():
    # Accessing session data using session dictionary
    username = session.get('username')

    if username:
        return f"Hello {username}, you are logged in via session!"
    else:
        return "No session found. Please enter your name first."

@app.route('/clearsession')
def clearsession():
    # session.pop removes 'username' key from session storage
    session.pop('username', None)
    return "Session has been cleared!<br><a href='/'>Go back</a>"

if __name__ == '__main__':
    app.run(debug=True)