import speech_recognition
import pyttsx3
import pywhatkit
import datetime
import wikipedia

# Assistant name
assistName = 'friday'

# Initialize voice recognizer and voice engine
listener = speech_recognition.Recognizer()
engine = pyttsx3.init()

# Voice selection and configuation
voices = engine.getProperty('voices')
engine.setProperty('voice' , voices[0].id)
engine. setProperty('rate', 200)
engine.setProperty('volume', 0.7)

# Valid options lists to voice recognizer
exitValidOptions = ['salir','exit','cerrar']
musicValidOptions = ['reproduce','escuchar','play']


# Initialize flag is true to execute loop code
flag = 1

def talk(text):
    """A simple function to permit assistant talk with a voice"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to the user's microphone and if says the name of the assistant correctly, execute the run function
    else, remember the assistant name to the user"""
    flag = 1

    try:
        with speech_recognition.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language='es-ES')
            rec = rec.lower()

            if assistName in rec:
                rec = rec.replace(assistName, '') 
                flag = run(rec)
            else:
                talk('Ese no es mi nombre, prueba a usar '+assistName)
    except:
        pass
    return flag

def run(command):
    """It reads the command that has been sent to it from the voice recognition and if there is an option it executes the corresponding function, 
    also, if the exit command is used, it returns a false as flag value, stopping the application, and else command not exist, return a message to
    say not understand."""
    if any(exit in command for exit in musicValidOptions):
        searchYoutube(command)
    elif 'hora' in command:
        hourTalk()
    elif 'busca' in command:
        searchWiki(command)
    elif any(exit in command for exit in exitValidOptions):
        flag = 0
        talk("Saliendo...")
    else:
        talk('Lo siento, no te he entendido')
    
    return flag

def searchYoutube(command):
    """Search for the text that has been given in the command on YouTube, opening a default browser tab with the first video that appears when searching"""
    music = command.replace('reproduce', '')
    print('Reproduciendo '+ music)
    talk('Reproduciendo'+music)
    pywhatkit.playonyt(music)

def searchWiki(command):
    """Search on the spanish wikipedia the value especified on the command and talk to the user"""
    order = command.replace('busca', '')
    wikipedia.set_lang("es")
    info = wikipedia.summary(order, 1)
    talk(info)

def hourTalk():
    """Takes the current time and returns it to the user using the talk function to speak"""
    hora = datetime.datetime.now().strftime('%I:%M %p')
    talk("Son las " + hora)

# While flag is true, execute listen function to assistant works
while flag:
    flag = listen()

