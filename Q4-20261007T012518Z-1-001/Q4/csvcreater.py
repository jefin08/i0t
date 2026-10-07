import requests
import pandas as pd

url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 9.93,
    "longitude": 76.27,
    "start_date": "2023-01-01",
    "end_date": "2025-12-31",
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "cloud_cover",
        "wind_speed_10m",
        "surface_pressure",
        "weather_code"
    ]
}

response = requests.get(url, params=params)
data = response.json()

df = pd.DataFrame({
    "time": data["hourly"]["time"],
    "temperature": data["hourly"]["temperature_2m"],
    "humidity": data["hourly"]["relative_humidity_2m"],
    "precipitation": data["hourly"]["precipitation"],
    "cloud_cover": data["hourly"]["cloud_cover"],
    "wind_speed": data["hourly"]["wind_speed_10m"],
    "surface_pressure": data["hourly"]["surface_pressure"],
    "weather_code": data["hourly"]["weather_code"]
})

df.to_csv("kochi_weather_2023_2025.csv", index=False)

print(df.head())
print("\nShape:", df.shape)
print("\nWeather codes:")
print(df["weather_code"].value_counts().sort_index())