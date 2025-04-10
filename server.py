import socket
import json
import requests
from datetime import datetime, timedelta

API_KEY = "197d5d7bc6df4c5281654303250904"
BASE_URL = "http://api.weatherapi.com/v1"

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5555
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
BUFFER_SIZE = 100000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
print(f"[LISTENING] Server running on {SERVER}:{PORT}")

def fetch_current(city):
    url = f"{BASE_URL}/current.json?key={API_KEY}&q={city}"
    return requests.get(url).json()

def fetch_forecast(city):
    url = f"{BASE_URL}/forecast.json?key={API_KEY}&q={city}&days=7"
    return requests.get(url).json()

def fetch_history(city):
    history_forecast = []
    today = datetime.today()
    for i in range(1, 8):  # past 7 days
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        url = f"{BASE_URL}/history.json?key={API_KEY}&q={city}&dt={date}"
        res = requests.get(url).json()
        try:
            day_info = res["forecast"]["forecastday"][0]["day"]
            history_forecast.append({
                "date": date,
                "day": {
                    "avgtemp_c": day_info["avgtemp_c"],
                    "condition": {
                        "text": day_info["condition"]["text"]
                    }
                }
            })
        except:
            continue
    return history_forecast

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        city = conn.recv(1024).decode(FORMAT)
        print(f"[REQUEST] City: {city}")

        current_data = fetch_current(city)
        forecast_data = fetch_forecast(city)
        history_data = fetch_history(city)

        # Future forecast formatting
        future_forecast = []
        for day in forecast_data.get("forecast", {}).get("forecastday", []):
            future_forecast.append({
                "date": day["date"],
                "day": {
                    "avgtemp_c": day["day"]["avgtemp_c"],
                    "condition": {
                        "text": day["day"]["condition"]["text"]
                    }
                }
            })

        combined = {
            "location": current_data.get("location", {}),
            "current": current_data.get("current", {}),
            "forecast": history_data + future_forecast  # Unified forecast format
        }

        conn.sendall(json.dumps(combined).encode(FORMAT))
    except Exception as e:
        print(f"[EXCEPTION] {e}")
    finally:
        conn.close()

while True:
    conn, addr = server.accept()
    handle_client(conn, addr)