import streamlit as st
import socket
import json
import pandas as pd
from datetime import datetime

# Server config
SERVER_IP = "192.168.179.72"  # Change to your actual server IP
SERVER_PORT = 5555

# Emoji mapping
def get_emoji(condition):
    condition = condition.lower()
    if "sun" in condition or "clear" in condition:
        return "☀️"
    elif "partly" in condition or "cloudy" in condition:
        return "⛅"
    elif "cloud" in condition:
        return "☁️"
    elif "rain" in condition:
        return "🌧️"
    elif "thunder" in condition:
        return "⛈️"
    elif "snow" in condition:
        return "❄️"
    elif "fog" in condition or "mist" in condition:
        return "🌫️"
    else:
        return "🌈"

# Background color mapping
def get_background_color(condition):
    condition = condition.lower()
    if "sun" in condition or "clear" in condition:
        return "#FFF9C4"  # light yellow
    elif "rain" in condition or "drizzle" in condition:
        return "#BBDEFB"  # light blue
    elif "cloud" in condition:
        return "#ECEFF1"  # light gray
    elif "snow" in condition:
        return "#E0F7FA"  # light cyan
    elif "fog" in condition or "mist" in condition:
        return "#D7CCC8"  # soft brown
    else:
        return "#FFFFFF"  # default white

# Socket communication
def get_weather_from_server(city):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_IP, SERVER_PORT))
        client.send(city.encode('utf-8'))
        data = client.recv(100000).decode('utf-8')
        client.close()
        return json.loads(data)
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Streamlit app setup
st.set_page_config(page_title="14-Day Weather App", page_icon="🌦️")

# Input
st.title("🌦️ 14-Day Weather Forecast App")
city = st.text_input("Enter City Name")

# Main logic
if city:
    with st.spinner("Fetching weather data..."):
        weather_data = get_weather_from_server(city)

    if weather_data:
        location = weather_data["location"]
        current = weather_data["current"]
        forecast = weather_data["forecast"]

        condition = current.get('condition', {}).get('text', 'Unknown')
        bg_color = get_background_color(condition)

        # Change background color using markdown + inline CSS
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-color: {bg_color};
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        # Display current weather
        st.subheader(f"{location.get('name')}, {location.get('country')}")
        st.write(f"**Local Time:** {location.get('localtime')}")
        st.metric("🌡 Temperature", f"{current.get('temp_c')} °C")
        st.write(f"**Condition:** {condition}")
        st.write(f"💨 **Wind:** {current.get('wind_kph')} km/h ({current.get('wind_dir')})")
        st.write(f"💧 **Humidity:** {current.get('humidity')}%")
        st.write(f"🌞 **UV Index:** {current.get('uv')}")
        st.write(f"🌫 **Visibility:** {current.get('vis_km')} km")
        st.write(f"📊 **Pressure:** {current.get('pressure_mb')} mb")
        st.write(f"🌍 **Coordinates:** Lat {location.get('lat')}, Lon {location.get('lon')}")
        st.write(f"🕓 **Observation Time:** {current.get('last_updated')}")

        # Forecast - Horizontal layout
        st.subheader("📅 14-Day Forecast")
        cols_per_row = 5
        for i in range(0, len(forecast), cols_per_row):
            row = forecast[i:i+cols_per_row]
            columns = st.columns(len(row))
            for col, day in zip(columns, row):
                date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
                date_str = date_obj.strftime("%b %d")
                day_data = day.get("day", {})
                temp = day_data.get("avgtemp_c", "N/A")
                cond_text = day_data.get("condition", {}).get("text", "")
                emoji = get_emoji(cond_text)

                with col:
                    st.markdown(f"**{date_str}**")
                    st.markdown(f"{emoji}")
                    st.markdown(f"**{temp}°C**")
                    st.markdown(f"*{cond_text}*")

        # Line chart
        chart_data = []
        for day in forecast:
            try:
                date = pd.to_datetime(day["date"])
                temp = day["day"]["avgtemp_c"]
                chart_data.append({"date": date, "temp": temp})
            except:
                continue

        if chart_data:
            df = pd.DataFrame(chart_data).sort_values("date")
            st.line_chart(df.set_index("date")["temp"], use_container_width=True)
        else:
            st.warning("No valid forecast data available for chart.")
