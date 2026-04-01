#  Honey-Token Canary Generator for CI/CD:

##  Overview
This project is a **deception-based security system** that detects unauthorized access to sensitive credentials.  
It automatically injects fake (honey) credentials into GitHub repositories and monitors their usage in real time.

If a hacker or attacker tries to use these fake credentials, the system immediately triggers an alert with details like IP address, location, and timestamp.

---

##  Features

-  Automated Honey Token Injection (GitHub API)
-  Real-time Webhook Listener (Flask)
-  Instant Alerts via Telegram Bot
-  Dashboard for Attack Monitoring
-  GeoIP Tracking (attacker location)
-  Cloud Deployment (Render)
-  CI/CD Ready Architecture

---

##  How It Works

1. Injector script adds fake credentials to a GitHub repository.
2. Each credential contains a unique tracking URL.
3. When someone accesses the credential:
   - The URL is triggered
   - The Flask server captures the request
4. System logs:
   - IP address
   - Timestamp
   - Location (GeoIP)
5. A real-time alert is sent via Telegram.
6. The event is displayed on a web dashboard.

---

##  Project Structure

honey-cicd/
├── injector/
│ └── main.py # Injects honey tokens into GitHub
├── listener/
│ ├── app.py # Webhook listener + dashboard
│ ├── logs.db # SQLite database for logs
│ └── requirements.txt
├── README.md


---

##  Tech Stack

- Python 
- Flask 
- GitHub API (PyGithub)
- SQLite 
- Telegram Bot API 
- GeoIP API 
- Render (Deployment) 

---

##  Setup Instructions

1. Clone Repository:
```bash
git clone https://github.com/your-username/honey-cicd.git
cd honey-cicd

2️.Install Dependencies:
pip install -r listener/requirements.txt

3️. Run Listener:
cd listener
python app.py

4️. Run Injector:
cd ../injector
python main.py

## Live Demo:

 https://honey-cicd.onrender.com

# Dashboard:

Access:

https://honey-cicd.onrender.com/dashboard

#Displays:

Token ID
IP Address
Location
Time of attack

#Alert Example
🚨 HONEY TOKEN TRIGGERED!
ID: abc123
IP: 192.168.x.x
Location: India
Time: 2026-03-31

# Use Case
Detect leaked credentials
Monitor insider threats
Track unauthorized repo access
Enhance DevSecOps security

# Key Concept
Instead of preventing attacks, this system focuses on:
 Detecting and tracking attackers using deception
 
