import speech_recognition as sr
import pyttsx3
import pywhatkit
import cv2
import threading

engine = pyttsx3.init()
engine.setProperty('rate', 115)

def speak_with_video(text, video_path="subhash.mp4"):
    def play_video():
        window_name = "Subhash - AI Assistant"
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Cannot open video.")
            return

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow(window_name, frame)

            if cv2.waitKey(30) & 0xFF == 27: 
                break

        cap.release()
        cv2.destroyAllWindows()

    video_thread = threading.Thread(target=play_video)
    video_thread.start()

    engine.say(text)
    engine.runAndWait()

    video_thread.join()  

def listen_and_play_song():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        speak_with_video("Hey!! I am subhash. Tell the song you like to listen.")
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            speak_with_video(f"Playing {command} on YouTube")
            pywhatkit.playonyt(command)
        except sr.UnknownValueError:
            error = "Sorry, I couldn't understand that."
            print(error)
            speak_with_video(error)
        except sr.RequestError:
            error = "Network error. Please check your internet connection."
            print(error)
            speak_with_video(error)

if __name__ == "__main__":
    listen_and_play_song()
