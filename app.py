from flask import Flask, render_template, request, redirect, jsonify, Response
import sqlite3
import json
import os
import hashlib
import hmac
import base64
import time

app = Flask(__name__)

# Mini App Toolkit Configuration
MINI_APP_SECRET = "your-secret-key-here"  # In production, use environment variable
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

# 4️⃣ Mini App Toolkit Functions
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

# 5️⃣ Account Association Endpoint
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

# 6️⃣ Farcaster manifest endpoint
@app.route('/.well-known/farcaster.json')
def farcaster_manifest():
    manifest_path = os.path.join('.well-known', 'farcaster.json')
    try:
        with open(manifest_path, 'r') as f:
            manifest_data = json.load(f)
        
        # Generate fresh account association data
        payload = generate_account_association_payload()
        signature = generate_account_association_signature(payload)
        
        # Update manifest with fresh account association
        manifest_data["accountAssociation"] = {
            "header": "X-Farcaster-Account-Association",
            "payload": payload,
            "signature": signature
        }
        
        return jsonify(manifest_data)
    except FileNotFoundError:
        return jsonify({"error": "Manifest not found"}), 404

# 7️⃣ Farcaster Webhook Endpoint
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

# 8️⃣ Serve Farcaster images
@app.route('/icon.png')
def serve_icon():
    return app.send_static_file('IMG_1774.jpeg')

@app.route('/image.png')
def serve_image():
    return app.send_static_file('IMG_1774.jpeg')

@app.route('/splash.png')
def serve_splash():
    return app.send_static_file('IMG_1774.jpeg')

# 5️⃣ Run the app
if __name__ == '__main__':
    app.run(debug=True)
