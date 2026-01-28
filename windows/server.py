from fastapi import FastAPI
import carla
import random

app = FastAPI()

client = carla.Client("localhost", 2000)
client.set_timeout(10.0)
world = client.get_world()


camera = None  # referencia global

@app.post("/camera/set")
def set_camera(data: dict):
    global camera

    transform = carla.Transform(
        carla.Location(
            x=data["x"],
            y=data["y"],
            z=data["z"]
        ),
        carla.Rotation(
            pitch=data["pitch"],
            yaw=data["yaw"],
            roll=0
        )
    )

    camera.set_transform(transform)
    return {"ok": True}

@app.post("/spawn_vehicles")
def spawn_vehicles(n: int = 20):
    blueprints = world.get_blueprint_library().filter("vehicle.*")
    spawn_points = world.get_map().get_spawn_points()

    spawned = 0
    for _ in range(n):
        bp = random.choice(blueprints)
        sp = random.choice(spawn_points)
        if world.try_spawn_actor(bp, sp):
            spawned += 1

    return {"spawned": spawned}

@app.post("/traffic_lights/green")
def traffic_green():
    tls = world.get_actors().filter("traffic.traffic_light*")
    for tl in tls:
        tl.set_state(carla.TrafficLightState.Green)
        tl.set_green_time(30)
    return {"state": "green"}

@app.post("/traffic_lights/red")
def traffic_red():
    tls = world.get_actors().filter("traffic.traffic_light*")
    for tl in tls:
        tl.set_state(carla.TrafficLightState.Red)
        tl.set_red_time(30)
    return {"state": "red"}
