import socket
import ssl
import time
import os
import urllib3
import requests
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HOST = "192.168.25.158"
PORT = 5000

FILE_URL = "https://github.com/psf/requests/archive/refs/heads/main.zip"

INTERVAL = 5  # 1 hour
TOTAL_RUNS = 5   # 24 hours


def measure_latency():
    try:
        start = time.time()
        requests.get("https://www.google.com", timeout=10, verify=False)
        return (time.time() - start) * 1000
    except:
        return -1.0


def measure_download():
    try:
        start_time = time.time()
        response = requests.get(FILE_URL, stream=True, timeout=60, verify=False)

        total_bytes = 0
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                total_bytes += len(chunk)

        time_taken = time.time() - start_time

        file_size = total_bytes / (1024 * 1024)
        throughput = (total_bytes * 8) / (time_taken * 1_000_000) if time_taken > 0 else 0
        bandwidth = throughput * 1.1

        return file_size, time_taken, throughput, bandwidth

    except:
        return 0, 0, 0, 0


def send_to_server(message):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(20)
        sock.connect((HOST, PORT))

        secure_socket = context.wrap_socket(sock, server_hostname=HOST)

        time.sleep(0.5)

        secure_socket.sendall(message.encode())
        secure_socket.shutdown(socket.SHUT_WR)

        time.sleep(0.3)
        secure_socket.close()

        print("[SUCCESS] Data sent to server")

    except Exception as e:
        print("[ERROR] Failed to send data:", e)


def run_cycle(hour, client_id):
    print(f"\n[HOUR {hour}] {datetime.now()}")

    latency = measure_latency()
    file_size, time_taken, throughput, bandwidth = measure_download()

    message = (
        f"ClientID={client_id} | "
        f"Hour={hour} | "
        f"File={file_size:.2f}MB | "
        f"Time Taken={time_taken:.2f}s | "
        f"Throughput={throughput:.2f}Mbps | "
        f"Latency={latency:.2f}ms | "
        f"Bandwidth={bandwidth:.2f}Mbps"
    )

    print("[SEND]", message)
    send_to_server(message)


if __name__ == "__main__":
    CLIENT_ID = socket.gethostname()

    for hour in range(1, TOTAL_RUNS + 1):
        run_cycle(hour, CLIENT_ID)

        if hour < TOTAL_RUNS:
            print("[WAIT] Sleeping 1 hour...\n")
            time.sleep(INTERVAL)