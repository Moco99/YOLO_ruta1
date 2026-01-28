# CARLA – Smart Traffic Control con YOLO, prototipado rapido V1

Arquitectura distribuida para:
- Simulación de tráfico en CARLA (Windows)
- Control remoto desde macOS
- Visión por computadora (YOLO)
- Semáforos inteligentes

## Arquitectura

Windows:
- Corre CARLA Server
- Publica stream de cámara (HTTP)

Mac:
- Controla tráfico
- Ve stream
- Ejecuta YOLO
- Decide semáforos

## Requisitos generales
- Python 3.8+
- CARLA 0.9.14 (solo en Windows)
- Conectividad entre Windows y Mac (VPN recomendado)

## Flujo de trabajo
1. Windows: arrancar CARLA
2. Windows: ejecutar stream de cámara
3. Mac: conectar, ver video y controlar tráfico
