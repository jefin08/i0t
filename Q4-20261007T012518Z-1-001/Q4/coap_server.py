import asyncio
import json
import requests

from aiocoap import resource, Context, Message


LATITUDE = 9.93
LONGITUDE = 76.27

API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    "&current="
    "temperature_2m,"
    "relative_humidity_2m,"
    "precipitation,"
    "cloud_cover,"
    "wind_speed_10m,"
    "surface_pressure"
)


class WeatherResource(resource.Resource):

    async def render_get(self, request):

        print("\nCoAP GET request received")
        print("Fetching live data from Open-Meteo...")

        try:

            response = requests.get(
                API_URL,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            current = data["current"]

            weather_data = {
                "location": "Kochi",

                "time": current["time"],

                "temperature": current["temperature_2m"],

                "humidity": current["relative_humidity_2m"],

                "precipitation": current["precipitation"],

                "cloud_cover": current["cloud_cover"],

                "wind_speed": current["wind_speed_10m"],

                "surface_pressure": current["surface_pressure"]
            }

            print("Data received from Open-Meteo:")
            print(weather_data)

            return Message(
                payload=json.dumps(weather_data).encode("utf-8"),
                content_format=50
            )

        except Exception as e:

            print("Error:", e)

            error_data = {
                "error": str(e)
            }

            return Message(
                payload=json.dumps(error_data).encode("utf-8"),
                content_format=50
            )


async def main():

    root = resource.Site()

    root.add_resource(
        ["weather"],
        WeatherResource()
    )

    await Context.create_server_context(
        root,
        bind=("127.0.0.1", 5683)
    )

    print("----------------------------------------")
    print("       CoAP Weather Server")
    print("----------------------------------------")
    print("Server   : coap://127.0.0.1:5683")
    print("Resource : /weather")
    print("----------------------------------------")
    print("Waiting for CoAP GET request...")
    print("----------------------------------------")

    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())