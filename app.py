from flask import Flask, render_template, request, redirect, jsonify, Response
import sqlite3
import json
import os
import hashlib
import hmac
import base64
import time

app = Flask(__name__)

# Configure Flask for production
app.config['DEBUG'] = False

# Mini App Toolkit Configuration
MINI_APP_SECRET = os.environ.get('MINI_APP_SECRET', 'default-secret-key-for-development')
MINI_APP_URL = "https://portfolio-tau-self-82.vercel.app"

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

# 2️⃣ Test endpoint
@app.route('/test')
def test():
    return jsonify({"status": "ok", "message": "Flask app is working"})

# 3️⃣ Home page
@app.route('/')
def home():
    return render_template("index.html")

# 4️⃣ Projects page
@app.route('/projects')
def projects():
    projects = [
        {"name": "Project 1", "description": "Description of Project 1"},
        {"name": "Project 2", "description": "Description of Project 2"},
        {"name": "Project 3", "description": "Description of Project 3"}
    ]
    return render_template("projects.html", projects=projects)

# 5️⃣ Contact page
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

# 6️⃣ Mini App Toolkit Functions
def generate_account_association_payload():
    """Generate account association payload for Farcaster"""
    payload = {
        "url": MINI_APP_URL,
        "timestamp": int(time.time())
    }
    return base64.b64encode(json.dumps(payload).encode()).decode()

def generate_account_association_signature(payload):
    """Generate signature for account association"""
    signature = hmac.new(
        MINI_APP_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"0x{signature}"

# 7️⃣ Account Association Endpoint
@app.route('/api/account-association')
def account_association():
    """Handle Farcaster account association"""
    payload = generate_account_association_payload()
    signature = generate_account_association_signature(payload)
    
    response_data = {
        "header": "X-Farcaster-Account-Association",
        "payload": payload,
        "signature": signature
    }
    
    return jsonify(response_data)

# 8️⃣ Farcaster manifest endpoint (now served statically by Vercel)

# 9️⃣ Farcaster Webhook Endpoint
@app.route('/api/webhook', methods=['POST'])
def farcaster_webhook():
    """Handle Farcaster webhook interactions"""
    try:
        data = request.get_json()
        
        # Log the webhook data for debugging
        print(f"Farcaster webhook received: {data}")
        
        # Handle different types of interactions
        if data and 'untrustedData' in data:
            button_index = data['untrustedData'].get('buttonIndex', 1)
            
            # Route based on button clicked
            if button_index == 1:
                # View Projects button
                return jsonify({
                    "type": "frame",
                    "image": f"{MINI_APP_URL}/image.png",
                    "buttons": [
                        {
                            "label": "Back to Home",
                            "action": "link",
                            "target": f"{MINI_APP_URL}"
                        }
                    ]
                })
            elif button_index == 2:
                # Contact Me button
                return jsonify({
                    "type": "frame",
                    "image": f"{MINI_APP_URL}/image.png",
                    "buttons": [
                        {
                            "label": "Back to Home",
                            "action": "link",
                            "target": f"{MINI_APP_URL}"
                        }
                    ]
                })
        
        # Default response
        return jsonify({
            "type": "frame",
            "image": f"{MINI_APP_URL}/image.png",
            "buttons": [
                {
                    "label": "View Projects",
                    "action": "link",
                    "target": f"{MINI_APP_URL}/projects"
                },
                {
                    "label": "Contact Me",
                    "action": "link",
                    "target": f"{MINI_APP_URL}/contact"
                }
            ]
        })
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"error": "Webhook processing failed"}), 500

# 🔟 Farcaster images (now served statically by Vercel)

# 5️⃣ Run the app
if __name__ == '__main__':
    app.run(debug=True)

# For Vercel deployment
app = app
