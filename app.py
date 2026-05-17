from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os

app = Flask(__name__)

# FIX 1: Secret key environment variable se
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-only-for-dev')
API_KEY = os.environ.get('API_KEY', '')

DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123')")
    conn.execute("INSERT OR IGNORE INTO users VALUES (2, 'alice', 'password')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "<h1>DevSecOps Demo App</h1><p>Login at /login</p>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db()

        # FIX 2: Parameterized query — SQL injection fix
        query = "SELECT * FROM users WHERE username=? AND password=?"
        result = conn.execute(query, (username, password)).fetchone()
        conn.close()

        if result:
            # FIX 3: render_template_string se XSS fix
            return render_template_string("<h2>Welcome {{ name }}!</h2>", name=result[1])
        return "<h2>Login failed!</h2>"

    return '''
        <form method="POST">
            Username: <input name="username"><br><br>
            Password: <input name="password" type="password"><br><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # FIX 4: render_template_string se XSS fix
    return render_template_string("<h2>Search results for: {{ q }}</h2>", q=query)

# FIX 5: Debug endpoint remove kar diya
# /debug route bilkul hata diya

if __name__ == '__main__':
    init_db()
    # FIX 6: debug=False, host localhost only
    app.run(debug=False, host='127.0.0.1', port=5000)