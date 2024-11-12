from ultralytics import YOLO
import cv2
from util import get_car, read_license_plate, write_csv
from sort.sort import *
from collections import defaultdict, Counter
from datetime import datetime
import numpy as np
import torch

# Initialize the tracker and models
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Initialize the tracker and models on GPU
tracker = Sort()
car_model = YOLO('./car_detection_model/runs/detect/train5/weights/best.pt').to(device)
plate_model = YOLO('./runs/detect/train15/weights/best.pt').to(device)

# Initialize webcam
cap = cv2.VideoCapture(0)  # Use 0 for default webcam, or change to the correct index if needed

# Variables to store tracking and recognition information
car_entry_times = {} 
results = {}
plate_texts_by_car = defaultdict(lambda: Counter())

frame_num = -1
ret = True

try:
    while ret:
        frame_num += 1
        ret, frame = cap.read()
        if not ret:
            break  # Exit if the webcam feed is interrupted

        results[frame_num] = {}

        # Detect cars in the current frame
        car_detections = car_model(frame)[0]
        detections = []
        for car_detection in car_detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = car_detection
            detections.append([x1, y1, x2, y2])

        # Track the detected cars
        track_id = tracker.update(np.asarray(detections)) if detections else []

        # Detect license plates in the current frame
        license_plate_detections = plate_model(frame)[0]
        for license_plate in license_plate_detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate
            xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_id)
            
            if car_id != -1:
                # Record the entry time if it's a new car
                if car_id not in car_entry_times:
                    car_entry_times[car_id] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Extract the license plate region
                license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
                
                # Preprocess the license plate for text recognition
                license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                license_plate_crop_gray = cv2.equalizeHist(license_plate_crop_gray)
                _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)
                
                # Recognize text from the license plate
                license_plate_text, license_plate_score = read_license_plate(license_plate_crop_thresh)
                if license_plate_text is not None:
                    plate_texts_by_car[car_id][license_plate_text] += 1
                    if plate_texts_by_car[car_id][license_plate_text] >= 5: 
                        results[frame_num][car_id] = {
                            'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                            'license_plate': {
                                'bbox': [x1, y1, x2, y2],
                                'text': license_plate_text,
                                'bbox_score': score,
                                'text_score': license_plate_score
                            },
                            'entry_time': car_entry_times[car_id]
                        }
        
        # Optional: Display the current frame with detections
        cv2.imshow("Webcam Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit the webcam feed
            break

except KeyboardInterrupt:
    print("Interrupted by user")

# Release resources
cap.release()
cv2.destroyAllWindows()

# Write the results to a CSV file
write_csv(results, './live_feed_results.csv')
