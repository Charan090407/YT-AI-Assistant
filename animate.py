import pyttsx3
import cv2
import numpy as np
import time
import threading

# ========== Text-to-Speech Setup ==========
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Speech rate
voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)  # Optional: choose voice

# ========== Define Lip Coordinates ==========
X1, X2 = 250, 320  # Horizontal mouth region
Y1, Y2 = 235, 260  # Vertical mouth region

# ========== Generate Lip-Open Frame ==========
def create_open_mouth_frame(img):
    open_frame = img.copy()
    mouth = img[Y1:Y2, X1:X2]
    
    # Stretch mouth vertically
    mouth_open = cv2.resize(mouth, (X2 - X1, int((Y2 - Y1) * 1.6)))

    # Paste back into image
    new_y2 = Y1 + mouth_open.shape[0]
    if new_y2 < open_frame.shape[0]:  # Ensure within image bounds
        open_frame[Y1:new_y2, X1:X2] = mouth_open

    return open_frame

# ========== Speak + Animate Assistant ==========
def animate_anime_assistant(image_path, text):
    original = cv2.imread(image_path)
    original = cv2.resize(original, (512, 512))
    open_mouth = create_open_mouth_frame(original)

    # Speak in a thread
    def speak():
        engine.say(text)
        engine.runAndWait()

    t = threading.Thread(target=speak)
    t.start()

    print("🗣️ Assistant is speaking...")

    while t.is_alive():
        # Alternate between open and closed mouth
        cv2.imshow("Anime Assistant (Talking)", open_mouth)
        if cv2.waitKey(180) & 0xFF == 27: break
        cv2.imshow("Anime Assistant (Talking)", original)
        if cv2.waitKey(180) & 0xFF == 27: break

    print("✅ Done speaking.")
    cv2.imshow("Anime Assistant (Idle)", original)
    cv2.waitKey(1500)
    cv2.destroyAllWindows()

# ========== Main ==========
if __name__ == "__main__":
    animate_anime_assistant("anime.jpeg", "Hello! I am your anime assistant. What song would you like me to play?")
