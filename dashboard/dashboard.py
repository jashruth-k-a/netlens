from flask import Flask, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "database.db"))

print("[DASHBOARD DB PATH]", DB_PATH)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "dashboard.html")


@app.route("/api/records")
def get_records():
    conn = get_db()
    rows = conn.execute("SELECT * FROM downloads ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/busiest-hour")
def busiest_hour():
    conn = get_db()
    row = conn.execute("""
        SELECT hour, AVG(CAST(REPLACE(throughput,'Mbps','') AS FLOAT)) as avg_tp
        FROM downloads
        GROUP BY hour
        ORDER BY avg_tp ASC
        LIMIT 1
    """).fetchone()
    conn.close()

    if row:
        return jsonify({"busiest_hour": row["hour"]})
    return jsonify({"busiest_hour": None})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)