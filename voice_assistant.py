import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
import pandas as pd
import email_contacts  # A Python file that reads names and email id

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 4 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    
    speak("My name is Computer Voice Assistant. How may I help you?")

def takeCommand():
    '''
      It takes microphone input from the user and returns string output
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language = 'en-US')
        print(f"User said: {query}\n")
    
    except Exception as e:
        print("Say that again please...")
        return "None"
    
    return query

def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    f = open("Your_password.txt")  # Text file containing the pw
    x = f.readline()
    f.close()
    server.login("your-email-id@domain.com", x)
    if to in email_contacts.contact_names:
        to_address = email_contacts.df.loc[to]['E-mail']
        print(to_address)
        server.sendmail("your-email-id@domain.com", to_address, content)
        speak("Email has been sent")
    else:
        speak("There is no entry with this name.")
    server.close()

if __name__ == "__main__":
    
    wishMe()
    while True:
        query = takeCommand().lower()
        # Logic for executing tasks based on query
        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 2)
            webbrowser.open("wikipedia.org/wiki/"+query)
            speak("Acording to wikipedia...")
            print(results)
            speak(results)
        
        elif "open google" in query:
            webbrowser.open("www.google.com")
        
        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")
        
        elif "open facebook" in query:
            webbrowser.open("www.facebook.com")
        
        elif "play music" in query:
            my_music_dir = "C:\\Users\\User\\Music\\alan walker"
            my_songs = os.listdir(my_music_dir)
            print(my_songs)
            os.startfile(os.path.join(my_music_dir, my_songs[random.randrange(len(my_songs))]))   # make it random
        
        elif "the time" in query:
            my_str_time = datetime.datetime.now().strftime("%H:%M")
            speak(f"Right now it's {my_str_time}")
        
        elif "the date" in query:
            my_str_time = datetime.datetime.now().strftime("%a, %d %b %Y")
            speak(f"Today is {my_str_time}")
        
        elif "open code" in query:
            # Open Visual Studio Code
            VSCode_Path = "Full\\Path\\Of\\The\\File"
            os.startfile(VSCode_Path)

        elif "open notepad" in query:
            # Open Notepad
            Notepad_path = "Full\\Path\\Of\\The\\File"
            os.startfile(Notepad_path)

        elif "open word" in query:
            # Open ms-word
            ms_word_path = "Full\\Path\\Of\\The\\File"
            os.startfile(ms_word_path)
        
        elif "send email" in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak("Who do you want to send this email to?")
                to = takeCommand()
                sendEmail(to, content)
            
            except Exception as e:
                speak("Sorry! Email cannot be sent.")
        
        elif "quit" in query:
            exit()
