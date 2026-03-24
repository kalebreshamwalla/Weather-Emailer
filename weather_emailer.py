import requests
import smtplib
import ssl
from datetime import datetime


# -----------------------------
# CONFIGURATION
# -----------------------------
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_gmail_app_password"
RECIPIENT_EMAIL = "recipient_email@example.com"


# -----------------------------
# AUTO-DETECT LOCATION
# -----------------------------
def get_current_location():
    try:
        ip_data = requests.get("https://ipapi.co/json/", timeout=10).json()
        lat = ip_data["latitude"]
        lon = ip_data["longitude"]
        city = ip_data["city"]
        region = ip_data["region"]
        return lat, lon, f"{city}, {region}"
    except Exception:
        # fallback if API fails
        return 33.4255, -111.94, "Tempe, AZ"


# -----------------------------
# FETCH WEATHER DATA
# -----------------------------
def get_daily_weather(url, location_name):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        daily = data["daily"]
        date = daily["time"][0]
        high_c = daily["temperature_2m_max"][0]
        low_c = daily["temperature_2m_min"][0]
        rain = daily["precipitation_sum"][0]

        # Convert Celsius → Fahrenheit
        high_f = (high_c * 9/5) + 32
        low_f = (low_c * 9/5) + 32

        weather_report = (
            f"Weather Forecast for {location_name} — {date}\n"
            f"High: {high_f:.1f}°F\n"
            f"Low: {low_f:.1f}°F\n"
            f"Expected Rain: {rain} mm\n"
        )

        return weather_report

    except Exception as e:
        return f"Error retrieving weather data: {e}"


# -----------------------------
# SEND EMAIL (UTF‑8 FIX)
# -----------------------------
def send_email(subject, body):
    message = (
        f"Subject: {subject}\n"
        f"Content-Type: text/plain; charset=utf-8\n\n"
        f"{body}"
    )

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(
                SENDER_EMAIL,
                RECIPIENT_EMAIL,
                message.encode("utf-8")  # UTF‑8 encoding fix
            )
        print("Email sent successfully.")

    except Exception as e:
        print(f"Error sending email: {e}")


# -----------------------------
# MAIN WORKFLOW
# -----------------------------
def main():
    print("Retrieving weather...")

    # Auto-detect location
    lat, lon, location_name = get_current_location()

    # Build dynamic API URL
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        f"&timezone=auto"
    )

    # Fetch weather
    weather = get_daily_weather(weather_url, location_name)

    # Email subject
    subject = f"Daily Weather Update - {datetime.now().strftime('%Y-%m-%d')}"

    # Send email
    send_email(subject, weather)


if __name__ == "__main__":
    main()
