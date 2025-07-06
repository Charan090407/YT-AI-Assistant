# --- IMPORTS ---
import speech_recognition as sr
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from gtts import gTTS
from playsound import playsound
import tkinter as tk
from PIL import Image, ImageTk
import os

# --- Show Anime Assistant Image ---
def show_anime_character():
    window = tk.Tk()
    window.title("Anime Assistant")
    window.geometry("300x400")
    
    img = Image.open("anime.png")
    img = img.resize((300, 300), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(window, image=photo)
    label.pack()

    info = tk.Label(window, text="Anime Assistant Ready!", font=("Helvetica", 14))
    info.pack()

    window.after(4000, lambda: window.destroy())
    window.mainloop()

# --- Speak with Anime-style Voice ---
def anime_speak(text):
    tts = gTTS(text=text, lang='en', tld='co.uk')  # or tld='co.jp' for Japanese
    filename = "anime_voice.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

# --- Listen from Microphone ---
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        anime_speak("Tell me what song you want me to play.")
        print("🎤 Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except:
        anime_speak("Sorry, I couldn't understand.")
        return ""

# --- Spotify Auth ---
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="YOUR_SPOTIFY_CLIENT_ID",
    client_secret="YOUR_SPOTIFY_CLIENT_SECRET",
    redirect_uri="http://localhost:8888/callback",
    scope="user-read-playback-state,user-modify-playback-state"
))

# --- Play Song ---
def play_song(song_name):
    results = sp.search(q=song_name, limit=1, type='track')
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        uri = track['uri']
        sp.start_playback(uris=[uri])
        anime_speak(f"Playing {track['name']} by {track['artists'][0]['name']}")
    else:
        anime_speak("I couldn't find that song on Spotify.")

# --- MAIN ---
if __name__ == "__main__":
    show_anime_character()
    command = listen()
    if command:
        play_song(command)
