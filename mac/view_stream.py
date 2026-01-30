import os
import cv2
from dotenv import load_dotenv

load_dotenv()
IP_WINDOWS = os.getenv("IP_WINDOWS")

cap = cv2.VideoCapture(f"http://{IP_WINDOWS}:8000/video")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("CARLA - Camara Semaforo", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
