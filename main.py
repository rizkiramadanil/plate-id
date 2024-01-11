import cv2
import numpy as np
import datetime

from ultralytics import YOLO
from sort.sort import Sort
from vehicle_util import get_vehicle
from ocr_util import read_license_plate
from color_util import dominant_color, classification_color
from csv_handler import write_csv

results = {}
mot_tracker = Sort()
coco = YOLO("./models/yolov8n.pt")
license_plate_detection = YOLO("./models/license_plate_detection_model.pt")
video_upload = "./uploads/upload.mp4"
video_capture = cv2.VideoCapture(video_upload)

vehicles = [2, 3, 5, 7]
vehicle_types = {2: "Mobil", 3: "Motor", 5: "Bus", 7: "Truk"}

frame_number = -1
ret = True

while ret:
    frame_number += 1
    ret, frame = video_capture.read()

    if not ret:
        break

    if ret:
        current_time = datetime.datetime.now()
        date_detection = current_time.strftime("%Y-%m-%d")
        time_detection = current_time.strftime("%H:%M:%S")

        results[frame_number] = results.get(frame_number, {})
        detections = coco(frame)[0]
        detections_ = detections.boxes.data.tolist() if detections is not None else []
        track_ids = mot_tracker.update(np.asarray(detections_))
        
        license_plates = (
            license_plate_detection(frame)[0].boxes.data.tolist()
            if license_plate_detection(frame)[0] is not None
            else []
        )

        for detection in detections_:
            x1_lp, y1_lp, x2_lp, y2_lp, license_plate_bbox_score = detection[:5]
            lp_class_id = int(detection[5])

            if lp_class_id in vehicles:
                vehicle_type = vehicle_types.get(lp_class_id, "Unknown")

                matching_license_plates = [
                    lp
                    for lp in license_plates
                    if x1_lp < lp[0] < x2_lp and y1_lp < lp[1] < y2_lp
                ]

                for license_plate in matching_license_plates:
                    (
                        x1_lp,
                        y1_lp,
                        x2_lp,
                        y2_lp,
                        license_plate_bbox_score,
                        lp_class_id,
                    ) = license_plate[:6]

                    x1_v, y1_v, x2_v, y2_v, vehicle_id = get_vehicle(
                        license_plate, track_ids
                    )

                    if vehicle_id != -1:
                        license_plate_crop = frame[
                            int(y1_lp) : int(y2_lp), int(x1_lp) : int(x2_lp), :
                        ]

                        license_plate_dominant_color = dominant_color(
                            frame, [x1_lp, y1_lp, x2_lp, y2_lp]
                        )
                        license_plate_classification_color = classification_color(
                            license_plate_dominant_color
                        )

                        license_plate_crop_gray = cv2.cvtColor(
                            license_plate_crop, cv2.COLOR_BGR2GRAY
                        )
                        _, license_plate_crop_thresh = cv2.threshold(
                            license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV
                        )

                        (
                            license_plate_text,
                            license_plate_text_score,
                        ) = read_license_plate(license_plate_crop_thresh)

                        if license_plate_text is not None:
                            results[frame_number][vehicle_id] = {
                                "date_detection": date_detection,
                                "time_detection": time_detection,
                                "vehicle": {
                                    "vehicle_bbox": [x1_v, y1_v, x2_v, y2_v],
                                    "vehicle_type": vehicle_type,
                                },
                                "license_plate": {
                                    "license_plate_bbox": [x1_lp, y1_lp, x2_lp, y2_lp],
                                    "license_plate_bbox_score": license_plate_bbox_score,
                                    "license_plate_text": license_plate_text,
                                    "license_plate_text_score": license_plate_text_score,
                                    "license_plate_color": license_plate_classification_color,
                                },
                            }


video_capture.release()

write_csv(results, "./csv/base.csv")
