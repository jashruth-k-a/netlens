# 🌐 NetLens - Automated Network Download Analyzer

A Python-based network monitoring system that analyzes download performance patterns over time using **TCP Socket Programming, SSL Security, and Real Time Visualization**.

---

## 🚀 Project Overview

NetLens is designed to simulate real-world network conditions by automatically downloading a file at regular intervals and analyzing performance metrics such as:

* 📥 Download Speed (Throughput)
* ⏱️ Time Taken
* 📡 Latency
* 📊 Bandwidth Estimation

The system identifies **Network Congestion Trends** and highlights the **Busiest Hour** based on performance degradation.

---

## 🧠 Architecture

```
Client → Server → Database → Dashboard API → Web UI
```

### 🔹 Components

* **Client**

  * Downloads a fixed file periodically
  * Measures network performance
  * Sends data via TCP (SSL-secured)

* **Server**

  * Accepts multiple client connections
  * Processes incoming data
  * Stores logs in SQLite database

* **Dashboard Server**

  * Flask-based API
  * Fetches data from database
  * Provides endpoints for visualization

* **Frontend (Dashboard)**

  * Displays charts and statistics
  * Updates automatically at intervals
  * Highlights congestion patterns

---

## ✨ Features

* ✅ Automated scheduled downloads
* ✅ Multi-client support
* ✅ Secure communication using SSL/TLS
* ✅ Real-time dashboard updates
* ✅ Performance logging and analysis
* ✅ Congestion detection (Busiest Hour)
* ✅ Interactive charts (Chart.js)

---

## ⚙️ Technologies Used

* **Language:** Python
* **Networking:** TCP Sockets
* **Security:** SSL/TLS
* **Backend:** Flask
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript (Chart.js)

---

## 📂 Project Structure

```
netlens/
│
├── client.py        # Client script
├── server.py        # Main TCP + SSL server
├── dashboard.py             # Flask dashboard server
├── dashboard.html           # Frontend UI
├── certificates.py          # SSL certificate generator
│
├── certs/
│   ├── cert.pem
│   └── key.pem
│
└── database.db              # SQLite database
```

---

## 🛠️ Setup Instructions

### 1️⃣ Install Dependencies

```bash
pip install flask requests urllib3
```

---

### 2️⃣ Generate SSL Certificates (Run Once)

```bash
python certificates.py
```

---

### 3️⃣ Start the Server

```bash
python netlens_server.py
```

---

### 4️⃣ Start Dashboard

```bash
python dashboard.py
```

Open in browser:

```
http://localhost:8080
```

---

### 5️⃣ Run Client(s)

```bash
python netlens_client.py
```

---

## 🧪 Testing (Recommended)

For demo/testing, modify:

```python
INTERVAL = 5
TOTAL_RUNS = 5
```

For actual execution:

```python
INTERVAL = 3600
TOTAL_RUNS = 24
```

---

## 🌐 Multi-Client Setup

To simulate real-world congestion:

1. Connect multiple devices to same network
2. Update client `HOST` with server IP
3. Run client on each device

---

## 📊 Output

* 📈 Time-series graphs (Throughput & Latency)
* 📋 Session logs
* ⚠️ Alerts for high latency
* 🎯 Busiest Hour detection

---

## 🧠 Key Concept

The busiest hour is determined by:

> The time period with the **lowest average throughput**, indicating maximum network congestion.

---

## 🎯 Learning Outcomes

* Low-level socket programming (TCP)
* Secure communication using SSL/TLS
* Client-server architecture
* Real-time data visualization
* Network performance analysis

---

## 🚀 Future Improvements

* WebSocket-based real-time updates
* Cloud deployment
* Advanced anomaly detection
* Authentication & user roles

---

## License

MIT

---
Built by [Jashruth K A](https://github.com/jashruth-k-a)