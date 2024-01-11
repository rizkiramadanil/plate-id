import ast
import cv2
import numpy as np
import pandas as pd

def draw_border(
    img,
    top_left,
    bottom_right,
    color=(0, 191, 255),
    thickness=16,
    line_length_x=150,
    line_length_y=150,
):
    x1, y1 = top_left
    x2, y2 = bottom_right

    cv2.line(img, (x1, y1), (x1, y1 + line_length_y), color, thickness)
    cv2.line(img, (x1, y1), (x1 + line_length_x, y1), color, thickness)

    cv2.line(img, (x1, y2), (x1, y2 - line_length_y), color, thickness)
    cv2.line(img, (x1, y2), (x1 + line_length_x, y2), color, thickness)

    cv2.line(img, (x2, y1), (x2 - line_length_x, y1), color, thickness)
    cv2.line(img, (x2, y1), (x2, y1 + line_length_y), color, thickness)

    cv2.line(img, (x2, y2), (x2, y2 - line_length_y), color, thickness)
    cv2.line(img, (x2, y2), (x2 - line_length_x, y2), color, thickness)

    return img

csv_read = pd.read_csv("./results/result.csv")

video_upload = "./uploads/upload.mp4"
video_capture = cv2.VideoCapture(video_upload)
fourcc = cv2.VideoWriter_fourcc(*"h264")
fps = video_capture.get(cv2.CAP_PROP_FPS)
width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_result = cv2.VideoWriter("./results/result.mp4", fourcc, fps, (width, height))

license_plate = {}

for vehicle_id in np.unique(csv_read["vehicle_id"]):
    mode_plate_text = csv_read[csv_read["vehicle_id"] == vehicle_id]["license_plate_text"].mode().iloc[0]

    license_plate[vehicle_id] = {
        "license_plate_crop": None,
        "license_plate_text": mode_plate_text,
    }
    video_capture.set(
        cv2.CAP_PROP_POS_FRAMES,
        csv_read[
            (csv_read["vehicle_id"] == vehicle_id)
            & (csv_read["license_plate_text"] == mode_plate_text)
        ]["frame_number"].iloc[0],
    )
    ret, frame = video_capture.read()

    x1, y1, x2, y2 = ast.literal_eval(
        csv_read[
            (csv_read["vehicle_id"] == vehicle_id)
            & (csv_read["license_plate_text"] == mode_plate_text)
        ]["license_plate_bbox"]
        .iloc[0]
        .replace("[ ", "[")
        .replace("   ", " ")
        .replace("  ", " ")
        .replace(" ", ",")
    )

    license_plate_crop = frame[int(y1) : int(y2), int(x1) : int(x2), :]
    license_plate_crop = cv2.resize(
        license_plate_crop, (int((x2 - x1) * 300 / (y2 - y1)), 300)
    )

    license_plate[vehicle_id]["license_plate_crop"] = license_plate_crop

frame_number = -1
video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
ret = True
while ret:
    ret, frame = video_capture.read()
    frame_number += 1
    if ret:
        df_ = csv_read[csv_read["frame_number"] == frame_number]

        for row_indx in range(len(df_)):
            vehicle_x1, vehicle_y1, vehicle_x2, vehicle_y2 = ast.literal_eval(
                df_.iloc[row_indx]["vehicle_bbox"]
                .replace("[ ", "[")
                .replace("   ", " ")
                .replace("  ", " ")
                .replace(" ", ",")
            )

            draw_border(
                frame,
                (int(vehicle_x1), int(vehicle_y1)),
                (int(vehicle_x2), int(vehicle_y2)),
                (0, 191, 255),
                16,
                line_length_x=150,
                line_length_y=150,
            )

            x1, y1, x2, y2 = ast.literal_eval(
                df_.iloc[row_indx]["license_plate_bbox"]
                .replace("[ ", "[")
                .replace("   ", " ")
                .replace("  ", " ")
                .replace(" ", ",")
            )
            cv2.rectangle(
                frame, (int(x1), int(y1)), (int(x2), int(y2)), (45, 34, 210), 8
            )

            license_plate_crop = license_plate[df_.iloc[row_indx]["vehicle_id"]][
                "license_plate_crop"
            ]
            H, W, _ = license_plate_crop.shape

            try:
                display_below = int(vehicle_y1) - H - 100 <= 0

                if display_below:
                    frame[
                        int(vehicle_y2) + 100 : int(vehicle_y2) + H + 100,
                        int((vehicle_x2 + vehicle_x1 - W) / 2) : int(
                            (vehicle_x2 + vehicle_x1 + W) / 2
                        ),
                        :,
                    ] = license_plate_crop

                    frame[
                        int(vehicle_y2) + H + 100 : int(vehicle_y2) + H + 360,
                        int((vehicle_x2 + vehicle_x1 - W) / 2) : int((vehicle_x2 + vehicle_x1 + W) / 2),
                        :,
                    ] = (255, 255, 255)

                    (text_width, text_height), _ = cv2.getTextSize(
                        license_plate[df_.iloc[row_indx]["vehicle_id"]]["license_plate_text"],
                        cv2.FONT_HERSHEY_SIMPLEX,
                        3.2,
                        14,
                    )

                    cv2.putText(
                        frame,
                        license_plate[df_.iloc[row_indx]["vehicle_id"]]["license_plate_text"],
                        (
                            int((vehicle_x2 + vehicle_x1 - text_width) / 2),
                            int(vehicle_y2 + H + 232 + (text_height / 2)),
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        3.2,
                        (0, 0, 0),
                        14,
                    )

                else:
                    frame[
                        int(vehicle_y1) - H - 100 : int(vehicle_y1) - 100,
                        int((vehicle_x2 + vehicle_x1 - W) / 2) : int(
                            (vehicle_x2 + vehicle_x1 + W) / 2
                        ),
                        :,
                    ] = license_plate_crop

                    frame[
                        max(0, int(vehicle_y1) - H - 360) : int(vehicle_y1) - H - 100,
                        int((vehicle_x2 + vehicle_x1 - W) / 2) : int((vehicle_x2 + vehicle_x1 + W) / 2),
                        :,
                    ] = (255, 255, 255)

                    (text_width, text_height), _ = cv2.getTextSize(
                        license_plate[df_.iloc[row_indx]["vehicle_id"]][
                            "license_plate_text"
                        ],
                        cv2.FONT_HERSHEY_SIMPLEX,
                        3.2,
                        14,
                    )

                    cv2.putText(
                        frame,
                        license_plate[df_.iloc[row_indx]["vehicle_id"]][
                            "license_plate_text"
                        ],
                        (
                            int((vehicle_x2 + vehicle_x1 - text_width) / 2),
                            int(vehicle_y1 - H - 232 + (text_height / 2)),
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        3.2,
                        (0, 0, 0),
                        14,
                    )

            except Exception as e:
                print(f"Error: {e}")

        video_result.write(frame)
        frame = cv2.resize(frame, (1280, 720))

video_result.release()
video_capture.release()
