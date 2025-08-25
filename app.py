from flask import Flask, request, jsonify
from flask import send_file


app = Flask(__name__)

# This is the endpoint Mailgun will POST inbound emails to
@app.route('/inbound', methods=['POST'])
def inbound_email():
    # Mailgun sends data in form-encoded format
    sender = request.form.get('sender')
    subject = request.form.get('subject')
    body_plain = request.form.get('body-plain')
    recipient = request.form.get('recipient')

    print(f"Email received from: {sender}")
    print(f"To: {recipient}")
    print(f"Subject: {subject}")
    print(f"Body: {body_plain}")

    # Respond to Mailgun
    return jsonify({'status': 'success'}), 200
@app.route('/download_csv', methods=['GET'])
def download_csv():
    return send_file('emails.csv', as_attachment=True)

if __name__ == '__main__':
    # Run on localhost port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
