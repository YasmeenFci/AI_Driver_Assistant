import threading
from services.send import main as send_location

def send_location_async():
    threading.Thread(target=send_location, daemon=True).start()