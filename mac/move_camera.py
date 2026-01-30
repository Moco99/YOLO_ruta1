import requests
import os
from dotenv import load_dotenv

load_dotenv()

IP = os.getenv("IP_WINDOWS")
BASE = f"http://{IP}:8000"


try:
    # Mover la camara
    requests.post(f"{BASE}/camera/set", json={
    "x": 100,
    "y": 30,
    "z": 59,
    "pitch": -45,
    "yaw": 180
    })
    print("Se ha movido la cámara")
except Exception as e:
    print(f"Error al mover la cámara: {e}")


