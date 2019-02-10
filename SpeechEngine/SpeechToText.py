import speech_recognition as sr

def SpeechToText():
    """Get input from the users through microphone

    Returns
    -------
    return : str
        Users input sentence
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening .....")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text, True
        except sr.UnknownValueError:
            return "Sorry, could not recognize what you said", False
        except sr.RequestError:
            return "Check your internet connection", False
        except:
            return "Sorry could not recognize what you said", False
