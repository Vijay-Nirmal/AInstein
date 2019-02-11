import speech_recognition as sr
import os

def fromMicrophone():
    """
    Records audio from the microphone of the device this program is being run on,
    and converts the speech to text using google's stt

    Returns
    -------
    text : str
        The text after running STT
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

def fromAudioFile(location, telegram=True):
    """
    Runs STT on the file specified. Since Telegram encodes their
    audio as OGA, and r.record() only takes audio of the format
    .wav, .flac we had to convert it to .wav using ffmpeg

    Parameters
    ----------
    location : str
        The location of the audio file
    telegram: boolean
        A boolean indicating if we need to convert OGA to WAV
        (default=True)

    Returns
    -------
    text : str
        The text after running STT
    """
    if telegram:
        # We need to convert
        newLocation = location[:-3] + "wav"
        print("ffmpeg -i {} {}".format(location, newLocation))
        os.system("ffmpeg -i {} {}".format(location, newLocation))
    r = sr.Recognizer()
    audioFile = sr.AudioFile(newLocation)
    with audioFile as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you were saying"
    except sr.RequestError:
        return "Woops, the internet seems to be down, I'm not able to contact my overlords"
    except:
        return "Sorry, I couldn't understand what you were saying"
    
