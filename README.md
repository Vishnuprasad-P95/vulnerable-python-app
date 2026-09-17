# Vulnerable Python Application

⚠️ **WARNING**: This application intentionally contains security vulnerabilities for testing purposes only.
**DO NOT deploy to production or expose to the internet!**

## Purpose

This application is designed to test automated vulnerability detection and fixing tools.

## Known Vulnerabilities

### Dependency Vulnerabilities
- Django 3.1.0 - Multiple CVEs
- Flask 1.1.1 - Security issues
- Pillow 8.1.0 - CVE-2021-34552
- Jinja2 2.11.0 - CVE-2020-28493
- PyYAML 5.3 - CVE-2020-14343
- cryptography 3.2 - Outdated with known issues

### Code Vulnerabilities
1. **SQL Injection** (`/user/<user_id>`)
   - Direct string concatenation in SQL query
   - No parameterized queries

2. **Cross-Site Scripting (XSS)** (`/search`)
   - User input rendered without escaping
   - Template injection vulnerability

3. **Code Injection** (`/eval`)
   - User input passed to `eval()`
   - Remote code execution risk

4. **Arbitrary File Upload** (`/upload`)
   - No file type validation
   - No content validation

5. **Open Redirect** (`/redirect`)
   - Unvalidated URL redirects
   - Phishing risk

6. **Sensitive Data Exposure** (`/api/data`)
   - No authentication required
   - Plaintext passwords and secrets

7. **Hardcoded Credentials**
   - Database password in source
   - Secret key in source

8. **Insecure Configuration**
   - Debug mode enabled
   - Binding to all interfaces

## Installation

```bash
# DO NOT run this in production!
pip install -r requirements.txt
python app.py
```

## Testing Vulnerabilities

### SQL Injection
```bash
curl http://localhost:5000/user/1%20OR%201=1
```

### XSS
```bash
curl "http://localhost:5000/search?q=<script>alert('XSS')</script>"
```

### Code Injection
```bash
curl "http://localhost:5000/eval?code=__import__('os').system('ls')"
```

## Fixes Required

- Upgrade all dependencies to latest secure versions
- Use parameterized SQL queries
- Implement proper input validation and sanitization
- Remove eval() and use safe alternatives
- Add file upload validation
- Validate redirect URLs
- Implement authentication and authorization
- Use environment variables for secrets
- Disable debug mode in production
- Bind to localhost only for development

## License

MIT - For educational purposes only
