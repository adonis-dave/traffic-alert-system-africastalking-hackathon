# Traffic Alert System - AfricasTalking Hackathon

Welcome to the **Traffic Alert System**, created as part of the **Africa's Talking Hackathon**! This system provides real-time traffic updates through SMS, helping drivers stay informed about road conditions and traffic congestion. The system supports multiple roads and junctions, offering detailed traffic data including vehicle counts and congestion levels.

## Features

- Real-time traffic updates via SMS for various roads and junctions.
- Supports roads such as **MOROGORO ROAD**, **NYERERE ROAD**, **UBUNGO INTERCHANGE**, and others.
- Provides vehicle breakdowns (cars, trucks, buses, motorbikes) and congestion levels at each junction.
- Simple and easy-to-use SMS interface for traffic queries.
- "HI" command to get instructions on how to use the system.
- **Real-Time Dashboard**: A dashboard to monitor traffic data and view vehicle counts in real time.

## How It Works

1. **Send Road Name**: To get traffic updates for a specific road, send the road name via SMS (e.g., "MOROGORO ROAD").
2. **Receive Traffic Data**: The system responds with a traffic report for the road, including vehicle counts and congestion information at different junctions.
3. **Support**: Send 'HI' for instructions and a list of available roads.
4. **Dashboard**: A real-time dashboard allows monitoring of vehicle counts and congestion levels, helping track traffic trends across various roads.

## Screenshots

### 1. **Live Feed of Vehicles Being Counted and Tracked by YOLO Object Detection**
*This image showcases the live feed of cars being counted and tracked in real time using YOLO (You Only Look Once) object detection.*

![YOLO Object Detection Live Feed](assets\livefeed.jpg)

### 2. **Africa's Talking Simulation Showing Messages Sent to Drivers**
*This screenshot shows the SMS traffic messages sent to drivers, providing them with real-time updates on road conditions.*

![Africa's Talking SMS Simulation](assets\messages.png)

## Example Request

To inquire about traffic on **MOROGORO ROAD**, send the following SMS:

```
MOROGORO ROAD
```

The system will respond with traffic details, such as:

```
Traffic Alert - MOROGORO Road
Total Vehicles: 176
Vehicle Breakdown:
Cars: 106
Trucks: 55
Buses: 10
Motorbikes: 5
Timestamp: 2025-02-22T18:43:01.453797
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/iamricky17/traffic-alert-system-africastalking-hackathon.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables (API keys for Africa's Talking, etc.).
4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### POST `/traffic-data/{road_id}`

- **Description**: Receive traffic data for a specific road.
- **Parameters**:
  - `road_id`: The name of the road.
  - `data`: A dictionary containing vehicle count and vehicle breakdown details.

### POST `/sms/callback`

- **Description**: Handle incoming SMS queries and respond with the relevant traffic data for a given road.

## Road Data

Example of available roads with their congestion levels:

- **MOROGORO ROAD**
  - Science Junction: High congestion, 100 cars, 50 trucks
  - Morroco Junction: Low congestion, 6 cars, 5 trucks
- **NYERERE ROAD**
  - Junction A: No Traffic, 10 cars, 0 trucks
  - Junction B: Mid Traffic, 50 cars, 20 trucks
- **UBUNGO INTERCHANGE**
  - Junction X: Heavy Traffic, 389 cars, 50 trucks

## Contributing

Feel free to fork this project and contribute. If you have any bug fixes or improvements, create a pull request!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.