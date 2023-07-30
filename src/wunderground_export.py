#!/usr/bin/env python3

import requests
import json
import pandas as pd
from datetime import datetime
import os

def get_weather_data(api_key, station_id):
    base_url = "https://api.weather.com/v2/pws/history/all"
    # Get the current date in CCYYMMDD format
    current_date = datetime.now().strftime("%Y%m%d")
    payload = {
        "apiKey": api_key,
        "format": "json",
        "stationId": station_id,
        "units": "e",
        "date": current_date
    }

    try:
        response = requests.get(base_url, params=payload)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def write_json_to_file(json_data, file_name):
    with open(file_name, "w") as file:
        json.dump(json_data, file, indent=2)

def convert_json_to_csv(json_data, file_name):
    # Extract the key-value pairs from the JSON data
    flat_data = []
    for entry in json_data['observations']:
        flat_entry = {key: entry[key] for key in entry.keys()}
        flat_data.append(flat_entry)

    # Convert to DataFrame and write to CSV
    df = pd.DataFrame(flat_data)
    df.to_csv(file_name, index=False)

def main():
    # Pull API key from environment variable
    api_key = os.getenv("WEATHER_API_KEY")
    if api_key is None:
        print("Error: Weather API key not found in environment variable 'WEATHER_API_KEY'")
        return

    # Pull station ID from environment variable
    station_id = os.getenv("WEATHER_STATION_ID")
    if station_id is None:
        print("Error: Weather station ID not found in environment variable 'WEATHER_STATION_ID'")
        return
    
    # Pull data directory location from environment variable
    weather_data_directory = os.getenv("WEATHER_DATA_DIRECTORY")
    if weather_data_directory is None:
        print("Error: Weather data directory not found in environment variable 'WEATHER_DATA_DIRECTORY'")
        return

    weather_data = get_weather_data(api_key, station_id)
    if weather_data:
        # Print the retrieved data or process it as needed
        #print(weather_data)

        # Create the output directory if it doesn't exist
        os.makedirs(weather_data_directory, exist_ok=True)

        # Write JSON data to a file
        json_file_name = os.path.join(weather_data_directory, "weather_data.json")
        write_json_to_file(weather_data, json_file_name)

        # Convert JSON data to CSV
        csv_file_name = os.path.join(weather_data_directory, "weather_data.csv")
        convert_json_to_csv(weather_data, csv_file_name)

if __name__ == "__main__":
    main()

