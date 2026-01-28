import carla
import random
import time

client = carla.Client("IP_DE_WINDOWS", 2000)
client.set_timeout(10.0)

world = client.get_world()
blueprints = world.get_blueprint_library()

# Spawn vehículos
vehicle_bp = blueprints.filter("vehicle.*")
spawn_points = world.get_map().get_spawn_points()

vehicles = []
for i in range(20):
    bp = random.choice(vehicle_bp)
    transform = random.choice(spawn_points)
    vehicle = world.try_spawn_actor(bp, transform)
    if vehicle:
        vehicles.append(vehicle)

print(f"🚗 {len(vehicles)} vehículos creados")

# Control semáforos
traffic_lights = world.get_actors().filter("traffic.traffic_light*")

for tl in traffic_lights:
    tl.set_state(carla.TrafficLightState.Green)
    tl.set_green_time(20)

print("🚦 Semáforos en verde")
