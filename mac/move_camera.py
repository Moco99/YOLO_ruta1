import requests
import os
from dotenv import load_dotenv

load_dotenv()

IP = os.getenv("IP_WINDOWS")
BASE = f"http://{IP}:8000"


try:
    # Mover la camara
    requests.post(f"{BASE}/camera/set", json={
    #yaw 70 y pitch -30
    # x se mueve de derecha a izquierda, mayor es a la izquierda y menor a la derecha
    # y se mueve de adelante para atras,a mayor es adelante y menor hacia attas
    # z se mueve de arriba a abajo, mayor es arriba y abajo es abajo
    "x": 50, 
    "y": 10,
    "z": 250,
    "pitch": -70, #inclinacion de la camara, arriba o abajo, (negativo es hacia abajo, positivo hacia arriba)
    "yaw": 90 # gira hacia la derecha o izquierda, entre mayor el numero mas a la derecha, entre mas pequeño mas a la izquierda
    })
    print("Se ha movido la cámara")
except Exception as e:
    print(f"Error al mover la cámara: {e}")


