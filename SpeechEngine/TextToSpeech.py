import pyttsx3

def TextToSpeech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.setProperty('rate', 60)
    engine.runAndWait()
