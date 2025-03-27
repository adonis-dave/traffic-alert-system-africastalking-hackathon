# Traffic Monitoring System

An intelligent traffic monitoring system that uses computer vision to detect and track vehicles in real-time, helping manage traffic flow efficiently. The system uses YOLOv8 for object detection and can communicate with a remote API to share traffic data.

## Features

- Real-time vehicle detection and tracking
- Multiple vehicle type classification (cars, trucks, buses, motorbikes)
- Traffic density monitoring
- Automated traffic light state management
- API integration for data sharing
- Support for multiple road monitoring
- Real-time visualization with vehicle counts and traffic states

## Prerequisites

- Python 3.8+
- CUDA-capable GPU (optional, for faster processing)
- OpenCV
- PyTorch
- Ultralytics YOLO

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/traffic-monitoring-system.git
cd traffic-monitoring-system
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Make sure you have the YOLO weights file (`yolo11n.pt`) in your project directory.

2. Run the main script:
```bash
python sending_data_main.py
```

The system will:
- Start processing the video feed
- Display real-time vehicle detection and counting
- Show traffic monitoring information
- Communicate with the configured API endpoint

Press 'q' to quit the application.

## Configuration

The system can be configured through the following parameters in `sending_data_main.py`:

- `API_URL`: The endpoint for sending traffic data
- `road_id`: Identifier for the monitored road (default: "Ubungo")
- `skip_frames`: Number of frames to skip between detections (default: 10)
- Vehicle classes and their corresponding YOLO class IDs are configurable in the `TrafficMonitor` class

## Project Structure

```
├── sending_data_main.py     # Main application script
├── requirements.txt         # Python dependencies
├── yolo11n.pt              # YOLO model weights
├── test.py                 # Testing script
└── yolo-Weights/           # Additional YOLO weights directory
```

## How It Works

1. **Vehicle Detection**: Uses YOLOv8 to detect vehicles in video frames
2. **Vehicle Tracking**: Implements ByteTrack for consistent vehicle tracking
3. **Traffic Analysis**: 
   - Counts vehicles by type
   - Monitors traffic density
   - Compares traffic levels across different roads
4. **Traffic Management**:
   - Automatically adjusts traffic light states based on vehicle density
   - Communicates with external systems via API

## API Integration

The system sends traffic data to a configured API endpoint with the following information:
- Road ID
- Vehicle count
- Timestamp
- Vehicle types distribution
- Other roads' traffic status

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license here]

## Acknowledgments

- YOLOv8 by Ultralytics
- ByteTrack for object tracking
- OpenCV community 