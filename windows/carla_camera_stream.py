import carla
import numpy as np
import cv2
from flask import Flask, Response

app = Flask(__name__)
latest_frame = None

def camera_callback(image):
    global latest_frame
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = array.reshape((image.height, image.width, 4))
    latest_frame = array[:, :, :3]

@app.route('/video')
def video():
    def generate():
        while True:
            if latest_frame is not None:
                _, jpeg = cv2.imencode('.jpg', latest_frame)
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    blueprint_library = world.get_blueprint_library()
    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', '1280')
    camera_bp.set_attribute('image_size_y', '720')
    camera_bp.set_attribute('fov', '90')

    transform = carla.Transform(
        carla.Location(x=0, y=0, z=15),
        carla.Rotation(pitch=-45)
    )

    camera = world.spawn_actor(camera_bp, transform)
    camera.listen(camera_callback)

    print("📡 Stream disponible en http://IP:5000/video")
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
