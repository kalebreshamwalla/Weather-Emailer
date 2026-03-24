# Weather Emailer

Python script that fetches daily weather forecasts for your location and automatically emails a weather report.

## Features

- Auto-detects your location via IP (with a fallback)
- Fetches daily weather forecasts using Open-Meteo API
- Converts temperatures from Celsius to Fahrenheit
- Sends an email with UTF‑8 encoding
- Easy to customize recipient and sender credentials via `.env`

## Prerequisites

- Python 3.x
- Packages:

```bash
pip install requests python-dotenv
