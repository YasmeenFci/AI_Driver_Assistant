import cv2
import threading
import time
from ultralytics import YOLO
from PIL import Image

from services.audio_service import play_alert_sound, stop_alert_sound
from services.speech_service import speak_multiple_times
from services.send_location_service import send_location_async
from utils.gui_utils import update_label

model = YOLO("models/weights/drowsiness.pt")

def start_drowsiness(video_label):
    def process():
        cap = cv2.VideoCapture(0)
        drowsy_time = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            #frame = cv2.resize(frame, (460, 360))
            results = model(frame)
            annotated = results[0].plot()

            drowsy = False
            for box in results[0].boxes:
                if int(box.cls) == 1:
                    drowsy = True

            if drowsy:
                play_alert_sound()
                if drowsy_time is None:
                    drowsy_time = time.time()

                if time.time() - drowsy_time > 10:
                    #speak("Driver is drowsy")
                    send_location_async()
            else:
                stop_alert_sound()
                drowsy_time = None

            img = Image.fromarray(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
            update_label(video_label, img)

        cap.release()

    threading.Thread(target=process, daemon=True).start()