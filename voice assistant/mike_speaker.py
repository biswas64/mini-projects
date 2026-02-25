import speech_recognition as sr
import pyttsx3
engine = pyttsx3.init()
engine.setProperty("rate",150)

def mikeControl():
    r=sr.Recognizer()
    try:
            with sr.Microphone() as source:
                print("bot is running")
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=10, phrase_time_limit=5)
                command = r.recognize_google(audio).lower().strip()
                return command

    except Exception as e:
        print(e)
        return e

def speaker(command):
     try:
          engine.say(command)
          engine.runAndWait()
     except Exception as e:
          print(f"Error : {e}")

         