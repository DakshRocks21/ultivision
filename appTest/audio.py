from playsound import playsound
import os, time

def test():
    files = os.listdir("data/sound")

    for file in files:
        playsound(f"data/sound/{file}")
        time.sleep(1)