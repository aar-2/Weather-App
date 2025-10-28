import streamlit as st
import requests
from datetime import datetime

# --- Header Section ---
def head():
    st.title("⛅ Live Weather Dashboard")
    st.markdown("Get **real-time** weather updates with visuals 🌍")

# --- Function to Fetch Weather ---
def get_weather(city):
    try:
        response = requests.get(f"http://localhost:5000/weather?city={city}")
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.ConnectionError:
        st.error("🚫 Unable to connect to the weather server. Make sure your Flask app is running on port 5000.")
    except Exception as e:
        st.error(f"⚠️ Unable to fetch data: {e}")
    return None

# --- Main Section ---
def main():
    st.set_page_config(page_title="Weather App", page_icon="🌤️", layout="centered")

    head()
    city = st.text_input("🏙️ Enter your city name")

    if st.button("🔍 Get Weather"):
        if not city:
            st.warning("Please enter a city name first.")
            return

        result = get_weather(city)
        if not result:
            st.error("❌ No data received from the server.")
            return

        if "error" in result:
            st.error(f"⚠️ {result['error']}")
            return

        weather_data = result.get("data", {})
        cached = result.get("cached", False)

        # Detect malformed or stringified JSON
        if isinstance(weather_data, str):
            st.error("Received text instead of structured JSON. Check your Flask app response.")
            st.code(weather_data)
            return

        if "main" not in weather_data or "weather" not in weather_data:
            st.error("⚠️ Invalid weather data format.")
            st.json(weather_data)
            return

        st.info(f"Data Source: {'🗃️ Cached' if cached else '🌐 Live API'}")

        # --- Extract Info Safely ---
        name = weather_data.get("name", city)
        country = weather_data.get("sys", {}).get("country", "")
        temp = weather_data["main"].get("temp", "N/A")
        condition = weather_data["weather"][0].get("description", "Unknown").title()
        icon_code = weather_data["weather"][0].get("icon", "")
        humidity = weather_data["main"].get("humidity", "N/A")
        wind_speed = weather_data.get("wind", {}).get("speed", "N/A")
        dt = weather_data.get("dt")
        time = datetime.fromtimestamp(dt).strftime("%I:%M %p") if dt else "N/A"

        # --- Display Weather Visually ---
        st.markdown("---")
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader(f"📍 {name}, {country}")
            st.metric("🌡️ Temperature", f"{temp} °C")
            st.write(f"**Condition:** {condition}")
            st.write(f"💧 Humidity: {humidity}%")
            st.write(f"🌬️ Wind Speed: {wind_speed} m/s")
            st.write(f"🕓 Updated at: {time}")

        with col2:
            if icon_code:
                icon_url = f"https://openweathermap.org/img/wn/{icon_code}@4x.png"
                st.image(icon_url, caption=condition)
            else:
                st.warning("No weather icon available.")

        st.markdown("---")
        st.success("✅ Weather data updated successfully!")

# --- Run App ---
if __name__ == "__main__":
    main()
