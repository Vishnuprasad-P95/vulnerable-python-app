"""
Vulnerable Python Application for Testing
This application intentionally contains security vulnerabilities for testing purposes.
DO NOT use in production!
"""

import os
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# VULNERABILITY: Hardcoded credentials
DATABASE_PASSWORD = "admin123"
SECRET_KEY = "super-secret-key-12345"

app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    return "Vulnerable Test Application"


@app.route('/user/<user_id>')
def get_user(user_id):
    """
    VULNERABILITY: SQL Injection
    User input is directly concatenated into SQL query
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Vulnerable SQL query - string concatenation
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)

    result = cursor.fetchone()
    conn.close()
    return str(result)


@app.route('/search')
def search():
    """
    VULNERABILITY: Cross-Site Scripting (XSS)
    User input is rendered without escaping
    """
    query = request.args.get('q', '')

    # Vulnerable template rendering - no escaping
    template = f"""
    <html>
        <body>
            <h1>Search Results</h1>
            <p>You searched for: {query}</p>
        </body>
    </html>
    """

    return render_template_string(template)


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    VULNERABILITY: Arbitrary File Upload
    No validation of file type or content
    """
    file = request.files.get('file')
    if file:
        # No validation - accepts any file
        filename = file.filename
        file.save(os.path.join('/tmp', filename))
        return f"File {filename} uploaded successfully"
    return "No file provided"


@app.route('/eval')
def evaluate():
    """
    VULNERABILITY: Code Injection
    User input is evaluated as Python code
    """
    code = request.args.get('code', '1+1')

    # EXTREMELY DANGEROUS - never use eval with user input
    result = eval(code)

    return f"Result: {result}"


@app.route('/redirect')
def redirect_to():
    """
    VULNERABILITY: Open Redirect
    No validation of redirect URL
    """
    url = request.args.get('url', '/')

    # No validation of URL - can redirect anywhere
    from flask import redirect
    return redirect(url)


@app.route('/api/data')
def api_data():
    """
    VULNERABILITY: Sensitive Data Exposure
    API returns sensitive information without authentication
    """
    sensitive_data = {
        'users': [
            {'id': 1, 'username': 'admin', 'password': 'admin123', 'ssn': '123-45-6789'},
            {'id': 2, 'username': 'user', 'password': 'password', 'email': 'user@example.com'}
        ],
        'api_key': 'sk-1234567890abcdef',
        'database_url': 'postgresql://admin:password@localhost:5432/mydb'
    }

    return sensitive_data


if __name__ == '__main__':
    # VULNERABILITY: Debug mode enabled in production
    # VULNERABILITY: Binding to all interfaces (0.0.0.0)
    app.run(debug=True, host='0.0.0.0', port=5000)
