# from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# SQLite DB file
DB_FILE = "emails.db"

# Create table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inbound_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            recipient TEXT,
            subject TEXT,
            body TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB when app starts
init_db()

# Endpoint to receive inbound emails
@app.route('/inbound', methods=['POST'])
def inbound_email():
    sender = request.form.get('sender')
    subject = request.form.get('subject')
    body_plain = request.form.get('body-plain')
    recipient = request.form.get('recipient')

    # Insert email into SQLite
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO inbound_emails (sender, recipient, subject, body)
        VALUES (?, ?, ?, ?)
    ''', (sender, recipient, subject, body_plain))
    conn.commit()
    conn.close()

    print(f"Email received from: {sender} to: {recipient}")
    return jsonify({'status': 'success'}), 200

# Endpoint to fetch all stored emails (for testing)
@app.route('/emails', methods=['GET'])
def get_emails():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inbound_emails')
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows to a list of dictionaries
    result = [
        {"id": row[0], "sender": row[1], "recipient": row[2], "subject": row[3], "body": row[4]}
        for row in rows
    ]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
