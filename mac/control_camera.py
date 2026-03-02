import requests
import os
from dotenv import load_dotenv

load_dotenv()

IP = os.getenv("IP_WINDOWS")
BASE = f"http://{IP}:8000"


#me canse de mover la camara a mano asi que hice un script rapido para irlo moviendo con wasd (solo en posicion, la camara es a mano aun)
exitChar = "q"
intensityChar = "i"

x = 50
y = 20
z = 250

intensity = 1

print("w - adelante")
print("s - atras")
print("a - izquierda")
print("d - derecha")
print("i - auementar intensidad (1-5)")
print("q - salir")

while True:
    inputChar = input("Instruccion: ")
    if inputChar == exitChar:
        break
    elif inputChar == "w":
        y += 10*intensity
    elif inputChar == "s":
        y -= 10*intensity
    elif inputChar == "a":
        x += 10*intensity
    elif inputChar == "d":
        x -= 10*intensity
    elif inputChar == "i":
        print("Configure la intensidad (1-5): ")
        intensity = int(input())
        if intensity < 1 or intensity > 5:
            print("Intensidad no valida, se usara i = 1 por defecto")
            intensity = 1
    else:
        print("Instruccion no valida")

    #aca nomas copie y pegue el codigo de move_camera.py 
    try:
        # Mover la camara
        requests.post(f"{BASE}/camera/set", json={
        #yaw 70 y pitch -30
        # x se mueve de derecha a izquierda, mayor es a la izquierda y menor a la derecha
        # y se mueve de adelante para atras,a mayor es adelante y menor hacia attas
        # z se mueve de arriba a abajo, mayor es arriba y abajo es abajo
        "x": x, 
        "y": y,
        "z": z,
        "pitch": -70, #inclinacion de la camara, arriba o abajo, (negativo es hacia abajo, positivo hacia arriba)
        "yaw": 90 # gira hacia la derecha o izquierda, entre mayor el numero mas a la derecha, entre mas pequeño mas a la izquierda
        })
        #mostramos las coordenadas actuales
        print("Se ha movido la cámara")
        print("-" * 20)
        print(f"Posicion actual: x={x}, y={y}, z={z}")
        print("-" * 20)
    except Exception as e:
        print(f"Error al mover la cámara: {e}")
    
    
    