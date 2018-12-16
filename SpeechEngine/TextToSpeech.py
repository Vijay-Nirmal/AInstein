import pyttsx3

def TextToSpeech(text):
    """Convert given sentence into speech

    Parameters
    ----------
    request : str
        The sentence to be coverted into speech format
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.setProperty('rate', 60)
    engine.runAndWait()
