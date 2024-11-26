from flask import Flask, render_template, Response, request, jsonify
import cv2
from ultralytics import YOLO
from util import get_car, read_license_plate
from sort.sort import *
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import numpy as np
import torch
import tempfile
import os
from db_util import insert_vehicle, update_exit_time, get_active_vehicle_entry, search_by_vehicle_number, search_by_timeperiod

app = Flask(__name__)

# Initialize models and tracker
device = "cuda" if torch.cuda.is_available() else "cpu"
tracker = Sort()
car_model = YOLO('./car_detection_model/runs/detect/train5/weights/best.pt').to(device)
plate_model = YOLO('./runs/detect/train15/weights/best.pt').to(device)

# Global variables for live feed
live_cap = None
live_results = {}
live_car_entry_times = {}
live_plate_texts_by_car = defaultdict(lambda: Counter())
car_last_seen_times = {}
EXIT_THRESHOLD = timedelta(seconds=7)

# Your existing process_live_frame function remains the same
#[Previous process_live_frame function code remains unchanged]
def process_live_frame(frame):
    """Process a single frame for live ANPR with database integration"""
    current_time = datetime.now()
    
    # Detect cars
    car_detections = car_model(frame)[0]
    detections = []
    for car_detection in car_detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = car_detection
        detections.append([x1, y1, x2, y2])

    # Track cars
    track_ids = tracker.update(np.asarray(detections)) if detections else []

    # Detect license plates
    license_plate_detections = plate_model(frame)[0]
    detected_plates = []
    
    for license_plate in license_plate_detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate
        xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

        if car_id != -1:
            # Process license plate
            license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
            license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
            _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)
            
            license_plate_text, license_plate_score = read_license_plate(license_plate_crop_thresh)
            
            if license_plate_text is not None:
                live_plate_texts_by_car[car_id][license_plate_text] += 1
                
                # Update last seen time for the car
                car_last_seen_times[car_id] = current_time
                
                if live_plate_texts_by_car[car_id][license_plate_text] >= 5:
                    # Check if vehicle is already in database
                    active_entry = get_active_vehicle_entry(license_plate_text)
                    
                    if not active_entry:
                        # New vehicle entry
                        insert_vehicle(license_plate_text, current_time)
                    
                    # Add detection info for display
                    detected_plates.append({
                        'car_bbox': [xcar1, ycar1, xcar2, ycar2],
                        'plate_bbox': [x1, y1, x2, y2],
                        'text': license_plate_text,
                        'score': license_plate_score
                    })

    # Check for vehicles that have left
    for car_id, last_seen in list(car_last_seen_times.items()):
        if (current_time - last_seen) > EXIT_THRESHOLD:
            if car_id in live_plate_texts_by_car:
                # Get the most commonly detected plate text for this car
                vehicle_number = live_plate_texts_by_car[car_id].most_common(1)[0][0]
                active_entry = get_active_vehicle_entry(vehicle_number)
                
                if active_entry:
                    entry_id, _ = active_entry
                    update_exit_time(entry_id, last_seen)
                
                # Clean up tracking data
                del live_plate_texts_by_car[car_id]
                del car_last_seen_times[car_id]

    # Draw detections on frame
    for detection in detected_plates:
        # Draw car bbox
        cv2.rectangle(frame, 
                     (int(detection['car_bbox'][0]), int(detection['car_bbox'][1])),
                     (int(detection['car_bbox'][2]), int(detection['car_bbox'][3])),
                     (0, 255, 0), 2)
        
        # Draw license plate bbox
        cv2.rectangle(frame,
                     (int(detection['plate_bbox'][0]), int(detection['plate_bbox'][1])),
                     (int(detection['plate_bbox'][2]), int(detection['plate_bbox'][3])),
                     (0, 0, 255), 2)
        
        # Add text
        cv2.putText(frame, 
                   detection['text'],
                   (int(detection['plate_bbox'][0]), int(detection['plate_bbox'][1] - 10)),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    return frame

def generate_frames():
    """Generator function for live feed frames"""
    global live_cap
    
    while True:
        if live_cap is None or not live_cap.isOpened():
            break
            
        success, frame = live_cap.read()
        if not success:
            break
            
        processed_frame = process_live_frame(frame)
        
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index1():
    """Render main page with navigation"""
    return render_template('index1.html')
@app.route('/index')
def index():
    """Render main page with navigation"""
    return render_template('index.html')
@app.route('/live_feed')
def live_feed_page():
    """Render live feed page"""
    return render_template('live_feed.html')

@app.route('/video_upload')
def video_upload_page():
    """Render video upload page"""
    return render_template('video_upload.html')

@app.route('/video_feed')
def video_feed():
    """Route for live video feed"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_live_feed')
def start_live_feed():
    """Start the live feed"""
    global live_cap, live_results, live_car_entry_times, live_plate_texts_by_car, car_last_seen_times
    
    if live_cap is not None:
        live_cap.release()
    
    live_cap = cv2.VideoCapture(0)
    live_results = {}
    live_car_entry_times = {}
    live_plate_texts_by_car = defaultdict(lambda: Counter())
    car_last_seen_times = {}
    
    return jsonify({"status": "success"})

@app.route('/stop_live_feed')
def stop_live_feed():
    """Stop the live feed"""
    global live_cap
    
    if live_cap is not None:
        live_cap.release()
        live_cap = None
    
    return jsonify({"status": "success"})

@app.route('/search_vehicle', methods=['POST'])
def search_vehicle():
    """Search for vehicle by number"""
    vehicle_number = request.json.get('vehicle_number')
    if not vehicle_number:
        return jsonify({"error": "No vehicle number provided"})
    
    results = search_by_vehicle_number(vehicle_number)
    return jsonify({"results": results})

@app.route('/search_timeperiod', methods=['POST'])
def search_timeperiod():
    """Search for vehicles within a time period"""
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    
    if not start_time or not end_time:
        return jsonify({"error": "Start time and end time are required"})
    
    try:
        start_datetime = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        end_datetime = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
    except ValueError:
        return jsonify({"error": "Invalid datetime format"})
    
    results = search_by_timeperiod(start_datetime, end_datetime)
    return jsonify({"results": results})

@app.route('/process_video', methods=['POST'])
def process_video():
    """Process uploaded video"""
    if 'video' not in request.files:
        return jsonify({"error": "No video file uploaded"})
    
    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({"error": "No video file selected"})
    
    # Save uploaded file temporarily
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, "temp_video.mp4")
    video_file.save(temp_path)
    
    # Process video
    cap = cv2.VideoCapture(temp_path)
    results = {}
    detected_plates = set()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        processed_frame = process_live_frame(frame)
        
        for car_id in live_plate_texts_by_car:
            if live_plate_texts_by_car[car_id]:
                plate_text = live_plate_texts_by_car[car_id].most_common(1)[0][0]
                detected_plates.add(plate_text)
    
    cap.release()
    os.remove(temp_path)
    os.rmdir(temp_dir)
    
    live_plate_texts_by_car.clear()
    car_last_seen_times.clear()
    
    return jsonify({
        "status": "success",
        "detected_plates": list(detected_plates)
    })

if __name__ == '__main__':
    app.run(debug=True)