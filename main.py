from logging import exception

import pyttsx3
import speech_recognition as sr
import keyboard
import webbrowser
import os
import subprocess as sp
import  imdb
from datetime import datetime
from decouple import config
from conv import random_text
from random import choice

from online import find_my_ip, search_on_wikipedia, search_on_google,youtube,send_email,get_news

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.0)  # Volume range: 0.0 to 1.0
engine.setProperty('rate', 225)  # Speed of speech
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice (index may vary)

# Load environment variables
USER = config('USER', default='User')
HOSTNAME = config('BOT', default='Assistant')


# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to greet user based on time
def greet_me():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good Morning {USER}")
    elif 12 <= hour < 16:
        speak(f"Good Afternoon {USER}")
    elif 16 <= hour < 19:
        speak(f"Good Evening {USER}")
    else:
        speak(f"Hello {USER}")

    speak(f"I am {HOSTNAME}. How may I assist you, {USER}?")



listening = False

def start_listening():
    global listening
    listening = True
    print("started Listening...")

def stop_listening():
    global listening
    listening = False
    print("stopped Listening...")

keyboard.add_hotkey('p', start_listening)
keyboard.add_hotkey('s', stop_listening)

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            if not 'stop' in query or 'exit' in query:
                speak(choice(random_text))
            else:
                hour = datetime.now().hour
                if hour>=21 and hour<6:
                    speak("Good Night sir,Take care!")
                else:
                    speak("Have a nice day!")
                exit()
    except Exception:
        speak("Oops! I didn't get that. Please say again.")
        query='None'
    return query



# Run the greeting when the script is executed
if __name__ == "__main__":
    greet_me()
    while True:
        if listening:
            query = takecommand().lower()
            # Example of replacing local app opening with websites
            if "how are you" in query:
                speak("I am absolutely fine sir. What about you?")
            elif "open google" in query:
                speak(f"What do you want to play on google {USER}?")
                query = takecommand().lower()
                search_on_google(query)
            elif "wikipedia" in query:
                speak(f"What do you want to search on wikipedia sir?")
                search=takecommand().lower()
                results= search_on_wikipedia(search)
                speak(f"According to wikipedia,{results}")
                speak("I am printing in on terminal")
                print(results)
            elif "open youtube" in query:
                speak("What do you want to play youtube sir?")
                video=takecommand().lower()
                youtube(video)
            elif "open facebook" in query:
                speak("Opening Facebook...")
                webbrowser.open("https://www.facebook.com")
            elif "open discord website" in query:
                speak("Opening Discord website...")
                webbrowser.open("https://discord.com")
            elif "open instagram" in query:
                speak("Opening Instagram...")
                webbrowser.open("https://www.instagram.com")
            elif "open twitter" in query:
                speak("Opening Twitter...")
                webbrowser.open("https://www.twitter.com")
            elif "open armoury crate website" in query:
                speak("Opening Armoury Crate website...")
                webbrowser.open("https://www.asus.com/support/Armoury-Crate/")
            elif "ip address" in query:
                ip_address=find_my_ip()
                speak(f"Your IP address is: {ip_address['ip']}")
                print(f"Your IP address is: {ip_address['ip']}")

            elif "send an email" in query:
                speak("On what email address do you want to send sir?.Please enter in the terminal")
                receiver_add=input("Email address:")
                speak("what should be the subject sir ?")
                subject=takecommand().capitalize()
                speak("What is the message?")
                message = takecommand().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speak("something went wrong Please check the error loga")

            elif"give me news" in query:
                speak(f"I am reading out the latest headlines of today ,sir")
                speak(get_news())
                speak("I am printing it on screen sir")
                print(*get_news(),sep="\n")

import imdb

def speak(text):
    # Placeholder speak function
    print(f"SPEAK: {text}")

def takecommand():
    # Placeholder for voice recognition or text input
    return input("You: ")

def search_movie_info():
    if "movies" in query.lower():
        movies_db = imdb.IMDb()

        speak("Please tell me the movie name:")
        movie_name = takecommand()

        speak(f"Searching for {movie_name}...")
        movies = movies_db.search_movie(movie_name)

        if not movies:
            speak("Sorry, I couldn't find any movie by that name.")
            return

        speak("I found the following results:")

        for movie in movies[:1]:  # Only showing the top result to avoid spamming
            title = movie.get('title', 'Unknown Title')
            year = movie.get('year', 'Unknown Year')
            movie_id = movie.movieID

            movie_info = movies_db.get_movie(movie_id)

            rating = movie_info.get('rating', 'No rating available')
            cast = movie_info.get('cast', [])[:5]
            cast_names = ', '.join(str(actor) for actor in cast)

            plot = movie_info.get('plot outline') or "Plot summary not available"

            output = (f"{title} was released in {year} and has an IMDb rating of {rating}. "
                      f"The main cast includes: {cast_names}. "
                      f"The plot summary is: {plot}.")

            speak(output)
            print(output)






