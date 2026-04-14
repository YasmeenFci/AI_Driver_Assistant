import cv2
import threading
import time
from ultralytics import YOLO
import easyocr
from PIL import Image, ImageTk

from services.speech_service import speak_multiple_times
from utils.gui_utils import update_label

VIDEO_PATH = "assets/videos/sign.mp4"
MODEL_PATH = "models/weights/sign.pt"
CLASS_NAMES = ['car', 'Motorcycle', 'bus', 'bicycle', 'truck', 'cat', 'delman', 'dog', 'pedestrian', 'red_traffic', 'yellow_traffic', 'speed limit', 'stop']

model = YOLO(MODEL_PATH)
reader = easyocr.Reader(['en'], gpu=False)
spoken_cache = set()
last_cache_clear = time.time()
speak_lock=threading.Lock() 


def start_sign(video_label):
    def process():
        cap = cv2.VideoCapture(VIDEO_PATH)
        global last_cache_clear
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if time.time() - last_cache_clear > 15:
                spoken_cache.clear()
                last_cache_clear = time.time()
            #frame=cv2.resize(frame,(380,400))
            results = model(frame)
            for r in results:
                for box in r.boxes:
                    conf = float(box.conf[0])
                    if conf < 0.5:
                        continue
                    cls_id = int(box.cls[0])
                    cls_name = CLASS_NAMES[cls_id]
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    label = cls_name
                    if cls_name == "speed limit":
                        cropped = frame[y1:y2, x1:x2]
                        if cropped.size == 0:
                            continue
                        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
                        _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
                        result = reader.readtext(thresh, detail=0)
                        text = " ".join(result)
                        number = ''.join(filter(str.isdigit, text))
                        if number:
                            label += f" {number}"
                            key = f"{cls_name}_{number}"
                            if key not in spoken_cache:
                                spoken_cache.add(key)
                                speak_multiple_times(f"Be careful, speed limit {number}")
                    else:
                        if cls_name not in spoken_cache:
                            spoken_cache.add(cls_name)
                            speak_multiple_times(f"Be careful, {cls_name}")
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            update_label(video_label, img)
        cap.release()
    threading.Thread(target=process, daemon=True).start()