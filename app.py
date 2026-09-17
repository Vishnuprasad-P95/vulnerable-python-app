"""
Python Application - security-hardened version
Originally contained intentional vulnerabilities for testing purposes.
This version fixes the critical/high issues reported in security scan.
"""

import ast
import os
import re
import sqlite3

from flask import Flask, request, render_template_string, redirect as flask_redirect
from markupsafe import escape
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Secrets should come from environment variables, not be hardcoded.
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')
app.config['SECRET_KEY'] = SECRET_KEY

ALLOWED_UPLOAD_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg', 'gif', 'pdf'}


def _allowed_file(filename: str) -> bool:
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS
    )


@app.route('/')
def index():
    return "Security-hardened Test Application"


@app.route('/user/<user_id>')
def get_user(user_id):
    """
    FIXED: SQL Injection
    User input is now passed as a bound parameter instead of being
    concatenated directly into the SQL string.
    """
    # Defense-in-depth: validate expected shape of the identifier.
    if not re.fullmatch(r'\d+', user_id):
        return "Invalid user id", 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Parameterized query - safe from SQL injection
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))

    result = cursor.fetchone()
    conn.close()
    return str(result)


@app.route('/search')
def search():
    """
    FIXED: Cross-Site Scripting (XSS)
    User input is now escaped before being rendered in HTML.
    """
    query = request.args.get('q', '')

    # Escape user input explicitly and rely on Jinja2 auto-escaping when
    # rendering it as a template variable (not by string interpolation).
    template = """
    <html>
        <body>
            <h1>Search Results</h1>
            <p>You searched for: {{ query }}</p>
        </body>
    </html>
    """

    return render_template_string(template, query=escape(query))


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    FIXED: Arbitrary File Upload
    Validates file extension and sanitizes filename before saving.
    """
    file = request.files.get('file')
    if file and file.filename:
        filename = secure_filename(file.filename)
        if not filename or not _allowed_file(filename):
            return "File type not allowed", 400

        upload_dir = os.environ.get('UPLOAD_DIR', '/tmp/uploads')
        os.makedirs(upload_dir, exist_ok=True)
        file.save(os.path.join(upload_dir, filename))
        return f"File {filename} uploaded successfully"
    return "No file provided", 400


@app.route('/eval')
def evaluate():
    """
    FIXED: Code Injection via eval()
    Uses ast.literal_eval() which only parses Python literals
    (numbers, strings, tuples, lists, dicts, booleans, None) and cannot
    execute arbitrary code.
    """
    code = request.args.get('code', '1+1')

    try:
        result = ast.literal_eval(code)
    except (ValueError, SyntaxError):
        return "Invalid expression: only literal values are supported", 400

    return f"Result: {result}"


@app.route('/redirect')
def redirect_to():
    """
    FIXED: Open Redirect
    Only allows relative, same-site redirect targets.
    """
    url = request.args.get('url', '/')

    # Reject absolute URLs / protocol-relative URLs to prevent redirecting
    # to attacker-controlled domains.
    if not url.startswith('/') or url.startswith('//'):
        url = '/'

    return flask_redirect(url)


@app.route('/api/data')
def api_data():
    """
    NOTE: This endpoint previously exposed sensitive data without
    authentication. It should require authentication/authorization in a
    real deployment. Sensitive values have been removed as an interim
    mitigation; add proper auth middleware before re-enabling real data.
    """
    return {
        'message': 'This endpoint requires authentication and has been disabled '
                    'pending implementation of proper access control.'
    }, 501


if __name__ == '__main__':
    # FIXED: debug mode and host binding are now controlled via environment
    # variables and default to safe values.
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', '5000'))
    app.run(debug=debug_mode, host=host, port=port)
