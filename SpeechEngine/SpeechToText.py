import speech_recognition as sr
import os

def fromMicrophone():
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
    
