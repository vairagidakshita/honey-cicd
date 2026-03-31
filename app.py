from flask import Flask, request, render_template_string
from datetime import datetime
import requests
import sqlite3

app = Flask(__name__)

BOT_TOKEN = "8766035086:AAEsa2trBkP1BvvaLz3KqpkR_CE8twAha4g"
CHAT_ID = "7711342956"

# 🗄️ DB setup
def init_db():
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id TEXT, ip TEXT, time TEXT, location TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 🌍 GeoIP function
def get_location(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return f"{res['city']}, {res['country']}"
    except:
        return "Unknown"

# 📩 Telegram alert
def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

# 🏠 Home
@app.route("/")
def home():
    return "Server is running 🚀"

# 🎯 Trigger
@app.route("/trigger/<id>")
def trigger(id):
    ip = request.remote_addr
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    location = get_location(ip)

    # Save to DB
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute("INSERT INTO logs VALUES (?, ?, ?, ?)", (id, ip, time, location))
    conn.commit()
    conn.close()

    alert = f"""
🚨 HONEY TOKEN TRIGGERED!
ID: {id}
IP: {ip}
Location: {location}
Time: {time}
"""

    print(alert)
    send_alert(alert)

    return "Logged", 200

# 📊 Dashboard
@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute("SELECT * FROM logs")
    data = c.fetchall()
    conn.close()

    html = """
    <h1>🚨 Attack Dashboard</h1>
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

if __name__ == "__main__":
    app.run(port=5000)