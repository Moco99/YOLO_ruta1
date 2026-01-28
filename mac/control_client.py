import requests

WINDOWS_IP = "100.x.x.x"  # Tailscale

# Aparecer autos
r = requests.post(f"http://{WINDOWS_IP}:8000/spawn_vehicles?n=30")
print(r.json())

# Semáforo en verde
requests.post(f"http://{WINDOWS_IP}:8000/traffic_lights/green")
