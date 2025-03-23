import requests
import json
import csv
url = "https://archive-api.open-meteo.com/v1/archive?latitude=26.2684&longitude=73.0059&start_date=2010-01-01&end_date=2025-03-21&daily=temperature_2m_max,temperature_2m_min,rain_sum"

response = requests.get(url)
data = response.json()
time = data["daily"]["time"]
max_temp = data["daily"]["temperature_2m_max"]
min_temp = data["daily"]["temperature_2m_min"]
rain = data["daily"]["rain_sum"]
with open("data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Max_Temperature", "Min_Temperature", "Rainfall"])
    for i in range(len(time)):
        writer.writerow([time[i], max_temp[i], min_temp[i], rain[i]])
        