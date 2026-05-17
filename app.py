from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'users.db'

# VULNERABILITY 1: Hardcoded secret key (Gitleaks isko pakde ga)
SECRET_KEY = "admin123password"
API_KEY = "sk-hardcoded-api-key-12345"

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
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        result = conn.execute(query).fetchone()
        conn.close()
        if result:
            return f"<h2>Welcome {result[1]}!</h2>"
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
    return f"<h2>Search results for: {query}</h2>"

@app.route('/debug')
def debug():
    return jsonify({
        "secret_key": SECRET_KEY,
        "api_key": API_KEY,
        "database": DATABASE
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)