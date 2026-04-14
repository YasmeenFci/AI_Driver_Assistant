import threading
from services.select_location_final import main as save_location_data


def save_location_async():
    threading.Thread(target=save_location_data, daemon=True).start()