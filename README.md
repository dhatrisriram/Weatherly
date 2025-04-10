# 🌦 Weatherly — 14-Day Weather Forecast Dashboard

Weatherly is a socket-based client-server weather monitoring system that provides detailed current weather conditions and a 14-day forecast (7 past + 7 future days) for any city entered by the user. Built using Python, Streamlit, and WeatherAPI, it offers a clean, interactive UI and real-time data visualization. Users can simply type a city name to instantly fetch weather insights, including temperature trends, humidity, wind data, UV index, and more.

---

## 📸 Features

- 🔎 Enter any city to get accurate weather data
- 🌐 Real-time client-server communication using Python sockets
- 🌬️ See temperature, humidity, pressure, wind, UV index, visibility, and more
- 📅 View current conditions, 7 days of past weather, and 7-day forecast
- 🎨 Dynamic background color that changes based on current weather conditions
- 📈 Beautifully rendered charts using Streamlit

---

## 🧰 Tech Stack

| Layer     | Technology          |
|-----------|---------------------|
| Backend   | Python, Socket, WeatherAPI |
| Frontend  | Streamlit           |
| Data      | JSON, WeatherAPI.com |
| Charts    | Pandas, Streamlit |

---
## 📦 How to Run Weatherly

### 1. Install the dependencies:
pip install streamlit pandas requests

### 2.Add your WeatherAPI key:
Replace (weather api key) in server.py with your actual API key.

### 3. Start the server
python server.py

### 4. Launch the Streamlit client
streamlit run client.py

---

## 🔐 API Used
WeatherAPI: https://www.weatherapi.com/

Endpoints used:

- current.json – for real-time weather
- forecast.json – for future forecast (up to 7 days)
- history.json – for past weather data (up to 7 days)







