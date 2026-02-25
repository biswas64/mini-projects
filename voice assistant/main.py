import mike_speaker as ms
import requests 
import time
import webbrowser

 #ths function gets the weather condtion  and  temperature of kathmandu
def weather_condition():
    city ="kathmandu"
    key = "-----------"
    try:
        res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric").json()
        temperature = res["main"]['temp']
        weather =res["weather"][0]["main"]
    except Exception as e:
        print(f"Error {e}")
    return temperature,weather

#we can ask time,date and day
def ask_time(command):
    if "time" in command:
        current = time.strftime("%H:%M")
        return current
    elif "date" in command:
        current = time.strftime("%Y:%m:%d")
        return current
    elif "day" in command:
        current = time.strftime("%A")
        return current
    
#it lets you open sites in browser and also we can search for things
def ask_browser(command):
    if len(command)>1 and command[0] == "open":
        required_site = command[1]
        try:
            webbrowser.open(f"https://www.{required_site}.com/")
        except Exception as e:
            print(f"Error: {e}")
        return required_site

    elif command[0] == "search":
        command.pop(0)
        required_search = " ".join(command)
        try:
            webbrowser.open(f"https://www.google.com/search?q={required_search}")
        except Exception as e:
            print(f"Error: {e}")
        return required_search
    else:
        return "invalid command"

    
def main():
    while True:
        try:  
            voice = ms.mikeControl()
            command = voice.split()
        except Exception as e:
            print(f"error :{e}")
            ms.speaker(f"Error occured")

        if voice == "deactivate":
            ms.speaker("...Deactivating")
            return
        else:
            if "open" in command or "search" in command:
                result = ask_browser(command)
                ms.speaker(f"opening {result}")
            elif "time" in command:
                result = ask_time(command)
                ms.speaker(f"its currently {result}")
            elif "temperature" in command or "weather" in command:
                temperature, weather = weather_condition()
                ms.speaker(f"the current temperature is {temperature}°Celcius")
                ms.speaker(f"and the weather shows {weather}")
            else:
                ms.speaker("invalid command")

if __name__ == "__main__":
        ms.speaker("Welcome user")
        main()

