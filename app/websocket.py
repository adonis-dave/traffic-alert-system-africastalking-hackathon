from fastapi import APIRouter, Request
import africastalking
import json
import os
from app.config import settings

# Initialize Africa's Talking
africastalking.initialize(
    username=settings.AT_USERNAME,
    api_key=settings.AT_API_KEY
)
sms = africastalking.SMS

# File path for the traffic data JSON file
TRAFFIC_DATA_FILE = "traffic_data.json"

# Function to load traffic data from the JSON file
def load_traffic_data():
    if os.path.exists(TRAFFIC_DATA_FILE):
        with open(TRAFFIC_DATA_FILE, "r") as file:
            return json.load(file)
    else:
        # Return default structure if file does not exist
        return {}

# Function to save traffic data to the JSON file
def save_traffic_data(data):
    with open(TRAFFIC_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Load traffic data at the start of the app
road_info = load_traffic_data()

TRAFFIC_PERSONNEL_NUMBERS = ["+255741827924"]  # Add traffic personnel's phone numbers here

# Define the router for API endpoints
router = APIRouter()

@router.post("/traffic-data/{road_id}")
async def receive_traffic_data(road_id: str, data: dict):
    """
    Receive traffic data from the monitoring system and send SMS alerts
    
    Expected data format:
    {
        "road_id": "east",
        "vehicle_count": 5,
        "timestamp": "2024-02-22T10:30:45.123456",
        "vehicle_types": {
            "car": 3,
            "truck": 1,
            "bus": 1,
            "motorbike": 0
        }
    }
    """
    try:
        # Construct SMS message
        sms_message = (f"Traffic Alert - {road_id.upper()} Road\n"
                       f"Total Vehicles: {data['vehicle_count']}\n"
                       f"Vehicle Breakdown:\n"
                       f"Cars: {data['vehicle_types']['car']}\n"
                       f"Trucks: {data['vehicle_types']['truck']}\n"
                       f"Buses: {data['vehicle_types']['bus']}\n"
                       f"Motorbikes: {data['vehicle_types']['motorbike']}\n"
                       f"Timestamp: {data['timestamp']}")
        
        # Send SMS to traffic personnel
        sms.send(sms_message, TRAFFIC_PERSONNEL_NUMBERS)
        print(f"🚀 SMS sent to traffic personnel: {sms_message}")
        
        # Update the traffic data in the road_info dictionary
        if road_id not in road_info:
            road_info[road_id] = {}

        # Update the specific road's traffic data
        road_info[road_id][data["timestamp"]] = {
            "congestion": "Unknown",  # You can customize this based on the data
            "number_of_cars": data["vehicle_types"]["car"],
            "number_of_trucks": data["vehicle_types"]["truck"],
            "time": data["timestamp"],
        }

        # Save the updated traffic data to the JSON file
        save_traffic_data(road_info)

        return {"status": "success", "message": "Traffic data received and processed"}
    
    except Exception as e:
        print(f"❌ Error processing traffic data: {str(e)}")
        return {"status": "error", "message": str(e)}

@router.post("/sms/callback")
async def sms_callback(request: Request):
    """Handles incoming SMS queries for traffic updates"""
    form_data = await request.form()
    print(f"Received SMS: {form_data}")
    message = form_data.get("text", "").strip().upper()
    from_number = form_data.get("from", "")

    # Check if the message is a known road name
    if message in road_info:
        road_data = road_info[message]
        response_message = f"Road Info for {message}:\n"
        
        # Format the info for each junction along the road
        for junction, info in road_data.items():
            response_message += (f"\n{junction}:\n"
                                 f"Congestion: {info['congestion']}\n"
                                 f"Number of Cars: {info['number_of_cars']}\n"
                                 f"Number of Trucks: {info['number_of_trucks']}\n"
                                 f"Time: {info['time']}\n")
    else:
        response_message = "Welcome to the Traffic Alert System! To get information about traffic on a specific road, send the name of the road. For example, send 'MOROGORO ROAD' to receive traffic updates. Here are some available roads you can inquire about:\n\n- MOROGORO ROAD\n- NYERERE ROAD\n- UBUNGO INTERCHANGE\n- BAGAMOYO ROAD\n- MSASANI HIGHWAY\n- MBEZI ROAD\n- PWANI ROAD\n- MASAKI ROAD\n- MIKOCHENI ROAD\n- PALM VILLAGE ROAD\n\nFor any questions or support, send 'HI' for instructions."
    
    try:
        sms.send(response_message, [from_number])
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
    
    return {"status": "success", "message": response_message}
