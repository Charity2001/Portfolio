from flask import Flask, render_template, request, redirect, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# 1️⃣ Create a database with a table (only runs once)
def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL
            );
        """)
init_db()

# 2️⃣ Home page
@app.route('/')
def home():
    return render_template("index.html")

# 3️⃣ Projects page
@app.route('/projects')
def projects():
    projects = [
        {"name": "Project 1", "description": "Description of Project 1"},
        {"name": "Project 2", "description": "Description of Project 2"},
        {"name": "Project 3", "description": "Description of Project 3"}
    ]
    return render_template("projects.html", projects=projects)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        with sqlite3.connect("database.db") as conn:
            conn.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
                         (name, email, message))
        return redirect('/')  # Redirect to home after sending
    return render_template("contact.html")

# 4️⃣ Farcaster manifest route
@app.route('/.well-known/farcaster.json')
def farcaster_manifest():
    return send_from_directory(
        os.path.join(app.root_path, '.well-known'),
        'farcaster.json',
        mimetype='application/json'
    )

# 5️⃣ Run the app
if __name__ == '__main__':
    app.run(debug=True)
