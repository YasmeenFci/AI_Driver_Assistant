import threading
import pyttsx3
import time

engine = pyttsx3.init()
speak_lock=threading.Lock() 
def speak_multiple_times(text, repeat=1, interval=2):
    def _speak():
        with speak_lock:
            print(f"🔊 [Thread] Speaking: {text}")
            for _ in range(repeat):
                engine.say(text)
                engine.runAndWait()
                time.sleep(interval)
    threading.Thread(target=_speak, daemon=True).start()
