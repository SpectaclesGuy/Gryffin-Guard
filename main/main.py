from ultralytics import YOLO
import cv2
from util import get_car, read_license_plate, write_csv
from sort.sort import *
from collections import defaultdict, Counter
from datetime import datetime

from skimage import io

tracker = Sort()  
car_model = YOLO('./car_detection_model/runs/detect/train5/weights/best.pt')
plate_model = YOLO('./runs/detect/train15/weights/best.pt')

cap = cv2.VideoCapture('./test_9.mp4')

car_entry_times = {} 
results = {}
ret = True
frame_num = -1
plate_texts_by_car = defaultdict(lambda: Counter())

while ret:
    frame_num += 1
    ret, frame = cap.read()
    if ret:
        results[frame_num] = {}
        car_detections = car_model(frame)[0]
        detections = []
        for car_detection in car_detections.boxes.data.tolist():
            #print(car_detections)
            x1, y1, x2, y2, score, class_id = car_detection
            detections.append([x1, y1, x2, y2])
        if detections:
            track_id = tracker.update(np.asarray(detections))
        license_plate = plate_model(frame)[0]
        for license_plate in license_plate.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate
            xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_id)
            if car_id != -1:
                if car_id not in car_entry_times:
                    car_entry_times[car_id] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
                #license plate processing
                license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                license_plate_crop_gray = cv2.equalizeHist(license_plate_crop_gray)
                _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)
                #license_plate_crop_thresh = cv2.adaptiveThreshold(
    #license_plate_crop_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
#)
                # cv2.imshow('original crop', license_plate_crop)
                # cv2.imshow('after threshold', license_plate_crop_thresh)
                # cv2.waitKey(0)
                license_plate_text, license_plate_score = read_license_plate(license_plate_crop_thresh)
                if license_plate_text is not None:
                    plate_texts_by_car[car_id][license_plate_text] += 1
                    if plate_texts_by_car[car_id][license_plate_text] >= 5: 
                        results[frame_num][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                'license_plate':{'bbox':[x1, y1, x2, y2], 
                                                                'text':license_plate_text, 
                                                                'bbox_score':score, 
                                                                'text_score':license_plate_score},
                                                                'entry_time': car_entry_times[car_id]  
                }
write_csv(results, './test_9.csv')