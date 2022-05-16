import time

import requests
import datetime
import smtplib

import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
password = os.environ.get("PASSWORD") # 環境変数
my_email = os.environ.get("MY_EMAIL")

LAT = 34.700836
LON = 135.493179
params = {
    "lat": LAT,
    "lon": LON
}


def night_time():
    now = datetime.datetime.now()
    response2 = requests.get(url="https://api.sunrise-sunset.org/json", params=params).json()
    sunset_hour = response2["results"]["sunset"].split(":")[0]
    sunrise_hour = response2["results"]["sunrise"].split(":")[0]
    if now.hour > int(sunset_hour) or now.hour < int(sunrise_hour):
        return True


def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json").json()
    iss_lat = float(response["iss_position"]["latitude"])
    iss_lon = float(response["iss_position"]["longitude"])
    if LAT - 3 <= iss_lat <= LAT + 3 and LON - 3 <= iss_lon <= LON + 3:
        return True


while True:
    time.sleep(60)
    if night_time() and iss_overhead():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"Subject:find ISS!\n\nLook Up!")
        break

