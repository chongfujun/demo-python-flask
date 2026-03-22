# Flask Blog Demo

A Flask blog application with intentional security patterns for testing static analysis tools.

## Purpose

This project demonstrates the difference between:
- **Real vulnerabilities** - Actual security issues
- **False positives** - Security tool alerts that aren't exploitable

Used for testing and evaluating security scanners like GitHub Advanced Security (CodeQL).

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000

## Security Testing

### CodeQL Scan Results
- ~21 alerts reported
- Only 1 real vulnerability (XSS)
- ~20 false positives

### Run POC
```bash
# Test XSS vulnerability
python poc_xss.py http://localhost:5000

# Test path traversal
python poc_path_traversal.py
```

## Vulnerability Types

| Type | Real | False Positive |
|------|------|----------------|
| XSS | 1 | 3 |
| Path Injection | 0 | 13 |
| Weak Hashing | 0 | 2 |
| XXE | 0 | 1 |
| SSRF | 0 | 1 |

See `POC_GUIDE.md` for details.