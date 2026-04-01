from flask import Flask, request, render_template_string
from datetime import datetime
import requests
import sqlite3
import os

app = Flask(__name__)

#  Secure credentials
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

#  Check if env variables exist
if not BOT_TOKEN or not CHAT_ID:
    print("⚠️ WARNING: BOT_TOKEN or CHAT_ID not set!")

#  Database setup
def init_db():
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id TEXT, ip TEXT, time TEXT, location TEXT)''')
    conn.commit()
    conn.close()

init_db()

#  Get location from IP
def get_location(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        city = res.get("city", "Unknown")
        country = res.get("country", "Unknown")
        return f"{city}, {country}"
    except:
        return "Unknown"

#  Send Telegram alert
def send_alert(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        res = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": message
        })
        print("📩 Telegram Response:", res.text)
    except Exception as e:
        print("❌ Telegram Error:", e)

#  Home route
@app.route("/")
def home():
    return "Server is running 🚀"

# Trigger route
@app.route("/trigger/<id>")
def trigger(id):
    ip = request.remote_addr
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    location = get_location(ip)

    # Save to database
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute("INSERT INTO logs VALUES (?, ?, ?, ?)", (id, ip, time_now, location))
    conn.commit()
    conn.close()

    alert = f"""
🚨 HONEY TOKEN TRIGGERED!
ID: {id}
IP: {ip}
Location: {location}
Time: {time_now}
"""

    print(alert)
    send_alert(alert)

    return "Logged", 200

#  Dashboard route
@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute("SELECT * FROM logs")
    data = c.fetchall()
    conn.close()

    html = """
    <h1 style="color:red;"> Attack Dashboard</h1>
    <table border="1" cellpadding="10">
        <tr>
            <th>Token ID</th>
            <th>IP</th>
            <th>Location</th>
            <th>Time</th>
        </tr>
        {% for row in data %}
        <tr>
            <td>{{row[0]}}</td>
            <td>{{row[1]}}</td>
            <td>{{row[3]}}</td>
            <td>{{row[2]}}</td>
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(html, data=data)

#  Run server (Render compatible)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
