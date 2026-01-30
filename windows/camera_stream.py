import carla
import numpy as np
import cv2
from flask import Flask, Response

# como ya mencione en server.py windows solo sera un servidor para CARLA y stremear la camara, aqui hacemos la parte de stremear la camara 

app = Flask(__name__)
frame = None

def camera_callback(image):
    global frame
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = array.reshape((image.height, image.width, 4))
    frame = array[:, :, :3]

@app.route("/video")
def video():
    def gen():
        while True:
            if frame is not None:
                _, jpeg = cv2.imencode(".jpg", frame)
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" +
                       jpeg.tobytes() + b"\r\n")
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")

def main():
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    bp = world.get_blueprint_library().find("sensor.camera.rgb")
    bp.set_attribute("image_size_x", "1280")
    bp.set_attribute("image_size_y", "720")

    transform = carla.Transform(carla.Location(z=15), carla.Rotation(pitch=-45))
    camera = world.spawn_actor(bp, transform)
    camera.listen(camera_callback)

    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
