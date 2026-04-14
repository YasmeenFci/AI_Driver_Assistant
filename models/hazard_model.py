
import cv2
import threading
from ultralytics import YOLO
from PIL import Image

from services.speech_service import speak_multiple_times
from services.save_location_service import save_location_async
from utils.gui_utils import update_label


model = YOLO("models/weights/hazard.pt")
video_path="assets/videos/hazard.mp4"
def start_hazard(video_label):
    def process():
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break
            frame = cv2.resize(frame, (600, 360))  # قللي الحجم
            results = model(frame)
            frame_area = frame.shape[0] * frame.shape[1]
            annotated_frame = frame.copy()

            for box in results[0].boxes:
                conf = float(box.conf[0])
                if conf < 0.5:
                    continue
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                box_area = (x2 - x1) * (y2 - y1)
                area_ratio = box_area / frame_area
                estimated_distance = round(max(0.3, min(5 * (1 - area_ratio), 5)), 1)
                label = f"{cls_name} - {estimated_distance} m"
                speak_multiple_times(f"Warning! {cls_name}, distance {estimated_distance} meters")
                threading.Thread(target=save_location_async, daemon=True).start()
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(annotated_frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            
            frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            update_label(video_label, img)
        cap.release()
    threading.Thread(target=process, daemon=True).start()
