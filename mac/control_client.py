import os
import requests
from dotenv import load_dotenv

load_dotenv()
IP = os.getenv("IP_WINDOWS")
BASE = f"http://{IP}:8000"


# spaw de autos
requests.post(f"{BASE}/spawn_vehicles?n=30")

# semaforos (luces)
requests.post(f"{BASE}/traffic/green")
# requests.post(f"{BASE}/traffic/red")
