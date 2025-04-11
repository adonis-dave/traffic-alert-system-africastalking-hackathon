from ultralytics import YOLO
import cv2
import torch
import time
import requests
from datetime import datetime

API_URL = "https://b297-197-186-3-135.ngrok-free.app"
class TrafficMonitor:
    def __init__(self, video_path, road_id="Ubungo"):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.model = YOLO("yolo11n.pt").to(self.device)
        self.vehicle_classes = ['car', 'truck', 'bus', 'motorbike']
        self.vehicle_class_ids = [2, 7, 5, 3]
        self.road_id = road_id
        self.skip_frames = 10
        self.frame_count = 0
        self.last_boxes = None
        
        # Hardcoded vehicle counts for other roads
        self.other_roads_vehicles = {
            "north": 5,
            "south": 10,
            "west": 7
        }
        
        # Traffic light states and configuration
        self.traffic_light_states = ["green", "yellow", "red"]
        self.current_light_state_index = 0

    def send_traffic_data(self, vehicle_count, vehicle_types):
        # Only send data if current road has more vehicles than other roads
        max_other_roads_vehicles = max(self.other_roads_vehicles.values())
        
        if vehicle_count > max_other_roads_vehicles:
            try:
                data = {
                    "road_id": self.road_id,
                    "vehicle_count": vehicle_count,
                    "timestamp": datetime.now().isoformat(),
                    "vehicle_types": vehicle_types,
                    "other_roads": self.other_roads_vehicles
                }
                response = requests.post(f"{API_URL}/traffic-data/{self.road_id}", json=data)
                print(f"Data sent: {data}")
                return response.json()
            except Exception as e:
                print(f"Error sending data to API: {e}")
        return None

    def process_frame(self, img, boxes):
        count = 0
        vehicle_types = {"car": 0, "truck": 0, "bus": 0, "motorbike": 0}
        
        if boxes and boxes.boxes:
            for box in boxes.boxes:
                cls = int(box.cls[0])
                class_name = self.vehicle_classes[self.vehicle_class_ids.index(cls)]
                count += 1
                vehicle_types[class_name] += 1
                
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
                
                track_id = box.id.int().item() if box.id is not None else None
                label = f'{class_name} #{track_id}'
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (255, 0, 0), 2)
        
        return count, vehicle_types

    def get_traffic_light_state(self, vehicle_count):
        # Find the maximum number of vehicles in other roads
        max_other_roads_vehicles = max(self.other_roads_vehicles.values())
        
        # Change light state if this road has significantly more vehicles
        if vehicle_count > max_other_roads_vehicles:
            self.current_light_state_index = (self.current_light_state_index + 1) % len(self.traffic_light_states)
        
        return self.traffic_light_states[self.current_light_state_index]

    def run(self):
        while True:
            success, img = self.cap.read()
            
            # If video ends, reset to the beginning
            if not success:
                self.cap.release()
                self.cap = cv2.VideoCapture(self.video_path)
                success, img = self.cap.read()
                # Reset frame count to avoid potential overflow
                self.frame_count = 0
            
            car_count = 0
            vehicle_types = {}
            
            if self.frame_count % self.skip_frames == 0:
                results = self.model.track(
                    img,
                    persist=True,
                    tracker="bytetrack.yaml",
                    conf=0.5,
                    iou=0.5,
                    classes=self.vehicle_class_ids,
                    verbose=False
                )
                if results:
                    self.last_boxes = results[0]
                    car_count, vehicle_types = self.process_frame(img, self.last_boxes)
                    self.send_traffic_data(car_count, vehicle_types)
            else:
                if self.last_boxes is not None:
                    car_count, vehicle_types = self.process_frame(img, self.last_boxes)

            # Get and display traffic light state
            light_state = self.get_traffic_light_state(car_count)
            
            # Display info
            cv2.putText(img, f'Vehicles: {car_count}', (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, f'Monitoring: {self.road_id.capitalize()} Road', (20, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Display other roads' vehicle counts
            other_roads_text = ', '.join([f"{road}: {count}" for road, count in self.other_roads_vehicles.items()])
            cv2.putText(img, f'Other Roads: {other_roads_text}', (20, 160), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            # Display traffic light state
            color = (0, 255, 0) if light_state == "green" else \
                    (0, 255, 255) if light_state == "yellow" else (0, 0, 255)
            

            cv2.imshow('Traffic Monitoring', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    monitor = TrafficMonitor("y2mate.com - Traffic Flow In The Highway  4K Stock Videos  NoCopyright  AllVideoFree_720pHFR.mp4")
    monitor.run()