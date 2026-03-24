import socket
import ssl
import sqlite3
import threading
import os

HOST = "0.0.0.0"
PORT = 5000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "database.db"))
CERT     = os.path.join(BASE_DIR, "..", "certs", "cert.pem")
KEY      = os.path.join(BASE_DIR, "..", "certs", "key.pem")

print("[SERVER DB PATH]", DB_PATH)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
db_lock = threading.Lock()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS downloads (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id  TEXT,
    hour       INTEGER,
    file_size  TEXT,
    time_taken TEXT,
    throughput TEXT,
    latency    TEXT,
    bandwidth  TEXT,
    timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=CERT, keyfile=KEY)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

print(f"[SERVER] Running on port {PORT}")


def parse_message(data):
    result = {}
    for part in data.split("|"):
        if "=" in part:
            key, _, value = part.partition("=")
            result[key.strip()] = value.strip()
    return result


def handle_client(client_socket, addr):
    print(f"[+] {addr}")

    try:
        try:
            secure_socket = context.wrap_socket(client_socket, server_side=True)
        except Exception as e:
            print("[SSL ERROR]", e)
            return

        data = secure_socket.recv(4096).decode()

        if not data:
            print("[WARNING] No data received")
            return

        print("[DEBUG RECEIVED]", data)

        parsed = parse_message(data)

        client_id  = parsed.get("ClientID", "unknown")
        hour       = parsed.get("Hour", "0")
        file_size  = parsed.get("File", "0MB")
        time_taken = parsed.get("Time Taken", "0s")
        throughput = parsed.get("Throughput", "0Mbps")
        latency    = parsed.get("Latency", "0ms")
        bandwidth  = parsed.get("Bandwidth", "0Mbps")

        with db_lock:
            cursor.execute(
                "INSERT INTO downloads (client_id, hour, file_size, time_taken, throughput, latency, bandwidth) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (client_id, hour, file_size, time_taken, throughput, latency, bandwidth)
            )
            conn.commit()

        print("[DB] Saved record")

        secure_socket.close()

    except Exception as e:
        print("[ERROR]", e)


while True:
    client_socket, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()