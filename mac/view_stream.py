import cv2

WINDOWS_IP = "100.x.x.x"  # Tailscale

cap = cv2.VideoCapture(f"http://{WINDOWS_IP}:5000/video")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("CARLA Stream", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
