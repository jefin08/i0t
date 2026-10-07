import asyncio
import json

import streamlit as st
import pandas as pd
import joblib

from aiocoap import Context, Message
from aiocoap.numbers.codes import Code


# ---------------------------------------
# Load Decision Tree Model
# ---------------------------------------

model = joblib.load("weather_decision_tree.pkl")


# ---------------------------------------
# CoAP Request Function
# ---------------------------------------

async def get_weather_from_coap():

    protocol = await Context.create_client_context()

    request = Message(
        code=Code.GET,
        uri="coap://127.0.0.1:5683/weather"
    )

    response = await protocol.request(request).response

    payload = response.payload.decode("utf-8")

    return json.loads(payload)


# ---------------------------------------
# Streamlit Page
# ---------------------------------------

st.set_page_config(
    page_title="CoAP Weather Classifier",
    page_icon="🌦️"
)


st.title("🌦️ CoAP-Based Weather Monitoring")
st.write("Live weather data from Open-Meteo through CoAP")


# ---------------------------------------
# Button
# ---------------------------------------

if st.button("Get Live Weather Data"):

    with st.spinner("Requesting data from CoAP Server..."):

        try:

            weather = asyncio.run(
                get_weather_from_coap()
            )

            # Check for server error
            if "error" in weather:

                st.error(weather["error"])

            else:

                st.success(
                    "Weather data received successfully!"
                )

                # ---------------------------------------
                # Display Time
                # ---------------------------------------

                st.subheader("Live Weather Data")

                st.write(
                    "Time:",
                    weather["time"]
                )


                # ---------------------------------------
                # Display Values
                # ---------------------------------------

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Temperature",
                        f'{weather["temperature"]} °C'
                    )

                with col2:
                    st.metric(
                        "Humidity",
                        f'{weather["humidity"]} %'
                    )

                with col3:
                    st.metric(
                        "Precipitation",
                        f'{weather["precipitation"]} mm'
                    )


                col4, col5, col6 = st.columns(3)

                with col4:
                    st.metric(
                        "Cloud Cover",
                        f'{weather["cloud_cover"]} %'
                    )

                with col5:
                    st.metric(
                        "Wind Speed",
                        f'{weather["wind_speed"]} km/h'
                    )

                with col6:
                    st.metric(
                        "Surface Pressure",
                        f'{weather["surface_pressure"]} hPa'
                    )


                # ---------------------------------------
                # Decision Tree Prediction
                # ---------------------------------------

                input_data = pd.DataFrame(
                    [[
                        weather["temperature"],
                        weather["humidity"],
                        weather["precipitation"],
                        weather["cloud_cover"],
                        weather["wind_speed"],
                        weather["surface_pressure"]
                    ]],
                    columns=[
                        "temperature",
                        "humidity",
                        "precipitation",
                        "cloud_cover",
                        "wind_speed",
                        "surface_pressure"
                    ]
                )


                prediction = model.predict(input_data)


                # ---------------------------------------
                # Display Prediction
                # ---------------------------------------

                st.subheader("Weather Classification")

                st.success(
                    f"Predicted Weather: {prediction[0]}"
                )


                # ---------------------------------------
                # Show Data Table
                # ---------------------------------------

                st.subheader("Data Received Through CoAP")

                st.dataframe(
                    input_data,
                    use_container_width=True
                )


        except Exception as e:

            st.error(
                f"CoAP connection failed: {e}"
            )