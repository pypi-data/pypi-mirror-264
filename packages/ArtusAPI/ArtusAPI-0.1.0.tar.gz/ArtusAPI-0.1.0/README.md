# Python Artus Robotic Hand API
This repository contains a Python API for controlling the Artus robotic hands.

## Directory Structure
```bash
├── ArtusAPI
│   ├── commnands
│   │   ├── commands.py # Command strings for the Robot Hand
│   ├── communication
│   │   ├── WiFi
│   │   │   ├── WiFi.py # WiFi communication class
│   │   ├── UART
│   │   │   ├── UART.py # UART communication class
│   │   ├── communication.py # Communication class for the API
│   ├── robot
│   │   ├── artus_3d
│   │   │   ├── artus_3d.py # Artus 3D Hand class
│   │   ├── artus_lite
│   │   │   ├── artus_lite.py # Artus Lite Hand class
│   │   ├── robot.py # Robot Hand class for the API
│   ├── artus_api.py # API Core

├── data
│   ├── grasp_poses
│   ├── images

├── examples
│   ├── example.py # Example usage of the API
```

## API Core
```python
class ArtusAPI()
```
