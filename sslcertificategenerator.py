"""
Run this ONCE to generate self-signed SSL certificates.
Certificates are saved in the certs/ folder.

Usage:
    python generate_certs.py
"""

import subprocess
import os

CERT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs")
os.makedirs(CERT_DIR, exist_ok=True)

CERT = os.path.join(CERT_DIR, "cert.pem")
KEY  = os.path.join(CERT_DIR, "key.pem")

if os.path.exists(CERT) and os.path.exists(KEY):
    print("[INFO] Certificates already exist:")
    print(f"  cert: {CERT}")
    print(f"  key:  {KEY}")
else:
    print("[INFO] Generating self-signed SSL certificate...")
    result = subprocess.run([
        "openssl", "req", "-x509",
        "-newkey", "rsa:2048",
        "-keyout", KEY,
        "-out",    CERT,
        "-days",   "365",
        "-nodes",
        "-subj",   "/CN=NetPulseServer"
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print("[OK] Certificates generated successfully:")
        print(f"  cert: {CERT}")
        print(f"  key:  {KEY}")
    else:
        print("[ERROR] Failed to generate certificates.")
        print(result.stderr)
        print("\nMake sure OpenSSL is installed:")
        print("  Windows: https://slproweb.com/products/Win32OpenSSL.html")
        print("  Linux:   sudo apt install openssl")
        print("  Mac:     brew install openssl")
