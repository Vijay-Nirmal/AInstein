import speech_recognition as sr

def SpeechToText():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening .....")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, could not recognize what you said"
        except sr.RequestError:
            return "Check your internet connection"
        except:
            return "Sorry could not recognize what you said"
