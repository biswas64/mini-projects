import requests
import schedule
import time
import os
from dotenv import load_dotenv
load_dotenv()
WEBHOOK_URL = os.getenv("webhook")


def api_call(lat,lon):
    try:
        url ="https://api.open-meteo.com/v1/forecast"
        params = {
        "latitude":lat,
        "longitude":lon,
        "hourly":"precipitation_probability,weathercode",
        "current_weather":True,
        "timezone":"auto"
            }
        req = requests.get(url,params=params,timeout=10)
        req.raise_for_status()
        data = req.json()
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"error ={e}")


def data_extractor(data):
    temp = data['current_weather']['temperature']
    rain = data['hourly']['precipitation_probability'][0]
    return temp,rain

def stored_message(temp,rain):
    messages = {
        "very cold":  f"brooo!!{temp}°C right now \n, its freeezing outside \n \n",
        "cold": f"{temp}°C right now \n pretty cold.So, wear something warm \n",
        "mild": f"{temp}°C right now, lovely right? \n",
        "hot": f"{temp}°C right now, getting hot outside \n",
        "very hot": f"broooo!!! {temp}°C right now \n  soooo hott outside. \n try not to faint ~tee-hee \n",
        "will rain":f"brooo,there is {rain}% chance to Rain next hour!\n Go with umbrellaa or raincoat  \n",
        "might rain": f"bro, around {rain}% chance to Rain  next hour!\n Be prepared \n",
        "no rain":f"There is {rain}% chance to rain,\n at least no need to worry about rain right?\n"
    }
    return messages

def weather_probability(temp,rain,messages):
    if temp > 32:
        message = messages["very hot"]
    elif temp > 28:
        message =  messages["hot"]
    elif temp > 18:
        message = messages["mild"]
    elif temp >= 9:
        message = messages["cold"]
    elif temp < 9:
        message =  messages["very cold"]

    if rain >=60:
        rain_message = messages["will rain"]
    elif rain >=20:
        rain_message =  messages["might rain"]
    elif rain >=0:
        rain_message =  messages["no rain"]
    message = message + rain_message

    return message


def send_text(message):

    if WEBHOOK_URL:
        try:
            text = {
                "content":message,

            }
            requests.post(WEBHOOK_URL,json=text)
        except requests.exceptions.RequestException as e:
            print(f"{e}")
    else:
        print("Couldn't fetch webhook")



def main():
    lat = 27.7017     #for kathmandu
    lon = 85.3206

    data = api_call(lat,lon)        
    if not data:
        return "Failed to fetch data"

    temp,rain = data_extractor(data)
    message = stored_message(temp,rain)
    texts = weather_probability(temp,rain,message)
    send_text(texts)

schedule.every().hour.do(main)
while True:
    schedule.run_pending()
    time.sleep(60)