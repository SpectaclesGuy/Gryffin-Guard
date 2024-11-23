from ultralytics import YOLO
import cv2
from util import get_car, read_license_plate, write_csv
from sort.sort import *
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from db_util import insert_vehicle, update_exit_time, get_active_vehicle_entry
from skimage import io

tracker = Sort()  
car_model = YOLO('./car_detection_model/runs/detect/train5/weights/best.pt')
plate_model = YOLO('./runs/detect/train15/weights/best.pt')

cap = cv2.VideoCapture('./test_9.mp4')

car_last_seen_times = {}
plate_texts_by_car = defaultdict(lambda: Counter())
EXIT_THRESHOLD = timedelta(seconds=7)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    car_detections = car_model(frame)[0]
    detections = []
    for car_detection in car_detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = car_detection
        detections.append([x1, y1, x2, y2])

    # Update the tracker
    track_id = tracker.update(np.asarray(detections)) if detections else []

    # License plate detection
    license_plate_detections = plate_model(frame)[0]
    for license_plate in license_plate_detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate
        xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_id)

        if car_id != -1:
            current_time = datetime.now()
            license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
            license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
            _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)
            license_plate_text, license_plate_score = read_license_plate(license_plate_crop_thresh)

            if license_plate_text is not None:
                plate_texts_by_car[car_id][license_plate_text] += 1

                if plate_texts_by_car[car_id][license_plate_text] >= 15:
                    # Check if this vehicle is already on campus
                    active_entry = get_active_vehicle_entry(license_plate_text)

                    if not active_entry:
                        # If no active entry, create a new one
                        insert_vehicle(license_plate_text, current_time)
                    else:
                        entry_id, last_seen_time = active_entry
                        car_last_seen_times[car_id] = current_time

    # Handle cars that have not been seen for more than the threshold
    current_time = datetime.now()
    for car_id, last_seen in list(car_last_seen_times.items()):
        if (current_time - last_seen) > EXIT_THRESHOLD:
            # Fetch the active entry to update its exit time
            vehicle_number = plate_texts_by_car[car_id].most_common(1)[0][0]
            active_entry = get_active_vehicle_entry(vehicle_number)
            
            if active_entry:
                entry_id, _ = active_entry
                update_exit_time(entry_id, last_seen)
            del car_last_seen_times[car_id]

cap.release()
cv2.destroyAllWindows()