from scipy.interpolate import interp1d
import csv
import numpy as np


def interpolate(data):
    frame_numbers = np.array([int(row["frame_number"]) for row in data])
    vehicle_ids = np.array([int(float(row["vehicle_id"])) for row in data])
    vehicle_bboxes = np.array(
        [list(map(float, row["vehicle_bbox"][1:-1].split())) for row in data]
    )
    license_plate_bboxes = np.array(
        [list(map(float, row["license_plate_bbox"][1:-1].split())) for row in data]
    )

    interpolated_data = []
    unique_vehicle_ids = np.unique(vehicle_ids)
    for vehicle_id in unique_vehicle_ids:
        frame_numbers_ = [
            p["frame_number"]
            for p in data
            if int(float(p["vehicle_id"])) == int(float(vehicle_id))
        ]

        vehicle_mask = vehicle_ids == vehicle_id
        vehicle_frame_numbers = frame_numbers[vehicle_mask]
        vehicle_bboxes_interpolated = []
        license_plate_bboxes_interpolated = []

        first_frame_number = vehicle_frame_numbers[0]
        last_frame_number = vehicle_frame_numbers[-1]

        for i in range(len(vehicle_bboxes[vehicle_mask])):
            frame_number = vehicle_frame_numbers[i]
            vehicle_bbox = vehicle_bboxes[vehicle_mask][i]
            license_plate_bbox = license_plate_bboxes[vehicle_mask][i]

            if i > 0:
                prev_frame_number = vehicle_frame_numbers[i - 1]
                prev_vehicle_bbox = vehicle_bboxes_interpolated[-1]
                prev_license_plate_bbox = license_plate_bboxes_interpolated[-1]

                if frame_number - prev_frame_number > 1:
                    frames_gap = frame_number - prev_frame_number
                    x = np.array([prev_frame_number, frame_number])
                    x_new = np.linspace(
                        prev_frame_number, frame_number, num=frames_gap, endpoint=False
                    )
                    interp_func = interp1d(
                        x,
                        np.vstack((prev_vehicle_bbox, vehicle_bbox)),
                        axis=0,
                        kind="linear",
                    )
                    interpolated_vehicle_bboxes = interp_func(x_new)
                    interp_func = interp1d(
                        x,
                        np.vstack((prev_license_plate_bbox, license_plate_bbox)),
                        axis=0,
                        kind="linear",
                    )
                    interpolated_license_plate_bboxes = interp_func(x_new)

                    vehicle_bboxes_interpolated.extend(interpolated_vehicle_bboxes[1:])
                    license_plate_bboxes_interpolated.extend(
                        interpolated_license_plate_bboxes[1:]
                    )

            vehicle_bboxes_interpolated.append(vehicle_bbox)
            license_plate_bboxes_interpolated.append(license_plate_bbox)

        for i in range(len(vehicle_bboxes_interpolated)):
            frame_number = first_frame_number + i
            row = {}
            row["frame_number"] = str(frame_number)
            row["vehicle_id"] = str(vehicle_id)
            row["vehicle_bbox"] = " ".join(map(str, vehicle_bboxes_interpolated[i]))
            row["license_plate_bbox"] = " ".join(
                map(str, license_plate_bboxes_interpolated[i])
            )

            if str(frame_number) not in frame_numbers_:
                row["date_detection"] = "0"
                row["time_detection"] = "0"
                row["vehicle_type"] = "0"
                row["license_plate_bbox_score"] = "0"
                row["license_plate_text"] = "0"
                row["license_plate_text_score"] = "0"
                row["license_plate_color"] = "0"
            else:
                original_row = [
                    p
                    for p in data
                    if int(p["frame_number"]) == frame_number
                    and int(float(p["vehicle_id"])) == int(float(vehicle_id))
                ][0]
                row["date_detection"] = (
                    original_row["date_detection"]
                    if "date_detection" in original_row
                    else "0"
                )
                row["time_detection"] = (
                    original_row["time_detection"]
                    if "time_detection" in original_row
                    else "0"
                )
                row["vehicle_type"] = (
                    original_row["vehicle_type"]
                    if "vehicle_type" in original_row
                    else "0"
                )
                row["license_plate_bbox_score"] = (
                    original_row["license_plate_bbox_score"]
                    if "license_plate_bbox_score" in original_row
                    else "0"
                )
                row["license_plate_text"] = (
                    original_row["license_plate_text"]
                    if "license_plate_text" in original_row
                    else "0"
                )
                row["license_plate_text_score"] = (
                    original_row["license_plate_text_score"]
                    if "license_plate_text_score" in original_row
                    else "0"
                )
                row["license_plate_color"] = (
                    original_row["license_plate_color"]
                    if "license_plate_color" in original_row
                    else "0"
                )

            interpolated_data.append(row)

    for i in range(1, len(interpolated_data)):
        for col in [
            "date_detection",
            "time_detection",
            "vehicle_type",
            "license_plate_bbox_score",
            "license_plate_text",
            "license_plate_text_score",
            "license_plate_color",
        ]:
            if interpolated_data[i][col] == "0":
                interpolated_data[i][col] = interpolated_data[i - 1][col]

    return interpolated_data


with open("./csv/base.csv", "r") as file:
    reader = csv.DictReader(file)
    original_data = list(reader)

interpolated_data = interpolate(original_data)

header = [
    "frame_number",
    "vehicle_id",
    "date_detection",
    "time_detection",
    "vehicle_bbox",
    "vehicle_type",
    "license_plate_bbox",
    "license_plate_bbox_score",
    "license_plate_text",
    "license_plate_text_score",
    "license_plate_color",
]

with open("./results/result.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    writer.writerows(interpolated_data)
