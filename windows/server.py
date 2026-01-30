from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import carla
import random
import numpy as np
import cv2
import time

# Lado servidor de carla (cliente) el cual recibira POST desde  macOS (OS que uso en mi otra lap) las instrucciones a ejecutarse en CARLA, windows solo
# servira como un servidor que corre carla, manda stream de video y aplica los cambios deseados.

# recordar que para que esto funcione remotamente y no solo dentro de la misma red es necesario usar un vpn (yo uso Tailscale) para no dejar los puertos
# abiertos. NUNCA LOS DEJEN ABIERTOS!!! Al usar el vpn usaremos la direccion IP que nos asigne, Tailscale te deja conectar los dispositivos de manera sencilla
# y una vez te de las IP, usas las direccione que te da para el servidor en la otra lap, en mi caso en macOS, aunque sin problema puede ser otro OS.

app = FastAPI()

# conectar a carla
client = carla.Client("localhost", 2000)
client.set_timeout(20.0)
world = client.get_world()

world_settings = world.get_settings()
world_settings.synchronous_mode = False
world.apply_settings(world_settings)


blueprints = world.get_blueprint_library()

# camara global
camera = None
latest_frame = None

camera_bp = blueprints.find("sensor.camera.rgb")
camera_bp.set_attribute("image_size_x", "1280")
camera_bp.set_attribute("image_size_y", "720")
camera_bp.set_attribute("fov", "90")

spawn_point = world.get_map().get_spawn_points()[0]
spawn_point.location.z += 12
spawn_point.rotation.pitch = -45

camera = world.try_spawn_actor(camera_bp, spawn_point)

if camera is None:
    raise RuntimeError("No se pudo crear la cámara. CARLA no está listo.")

# callback de imagen
def process_image(image):
    global latest_frame
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = array.reshape((image.height, image.width, 4))
    latest_frame = array[:, :, :3]

camera.listen(process_image)

# stream de video
def gen_frames():
    global latest_frame
    while True:
        if latest_frame is not None:
            _, jpg = cv2.imencode(".jpg", latest_frame)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + jpg.tobytes() + b"\r\n"
            )
        time.sleep(0.03)

@app.get("/video")
def video():
    return StreamingResponse(
        gen_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# control de la camara
@app.post("/camera/set")
def set_camera(data: dict):
    transform = carla.Transform(
        carla.Location(x=data["x"], y=data["y"], z=data["z"]),
        carla.Rotation(pitch=data["pitch"], yaw=data["yaw"], roll=0)
    )
    camera.set_transform(transform)
    return {"ok": True}

# spawn de autos
@app.post("/spawn_vehicles")
def spawn_vehicles(n: int = 20):
    blueprints = world.get_blueprint_library().filter("vehicle.*")
    spawn_points = world.get_map().get_spawn_points()

    traffic_manager = client.get_trafficmanager(8001)
    traffic_manager.set_synchronous_mode(False)

    spawned = 0
    for _ in range(n):
        bp = random.choice(blueprints)
        sp = random.choice(spawn_points)
        vehicle = world.try_spawn_actor(bp, sp)
        if vehicle:
            vehicle.set_autopilot(True, traffic_manager.get_port())
            spawned += 1

    return {"spawned": spawned}


# semafoross
@app.post("/traffic/green")
def traffic_green():
    for tl in world.get_actors().filter("traffic.traffic_light*"):
        tl.set_state(carla.TrafficLightState.Green)
        tl.set_green_time(30)
    return {"state": "green"}

@app.post("/traffic/red")
def traffic_red():
    for tl in world.get_actors().filter("traffic.traffic_light*"):
        tl.set_state(carla.TrafficLightState.Red)
        tl.set_red_time(30)
    return {"state": "red"}
