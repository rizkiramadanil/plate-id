import cv2
import numpy as np


def dominant_color(image, plate_bbox):
    x1, y1, x2, y2 = plate_bbox
    plate_crop = image[int(y1) : int(y2), int(x1) : int(x2), :]

    plate_height, plate_width, _ = plate_crop.shape

    center_ratio = 0.2

    center_x1 = int(plate_width * (1 - center_ratio) / 2)
    center_x2 = int(plate_width * (1 + center_ratio) / 2)
    center_y1 = int(plate_height * (1 - center_ratio) / 2)
    center_y2 = int(plate_height * (1 + center_ratio) / 2)

    center_crop = plate_crop[center_y1:center_y2, center_x1:center_x2, :]

    pixels = np.float32(center_crop.reshape(-1, 3))
    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    _, labels, centers = cv2.kmeans(
        pixels, n_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )
    center_counts = np.bincount(labels.flatten())
    dominant_color_index = np.argmax(center_counts)
    dominant_color = centers[dominant_color_index].astype(int)
    return dominant_color.tolist()


def classification_color(dominant_color):
    black_lower = np.array([0, 0, 0])
    black_upper = np.array([70, 70, 70])
    white_lower = np.array([80, 80, 80])
    white_upper = np.array([255, 255, 255])
    red_lower = np.array([0, 0, 40])
    red_upper = np.array([100, 100, 255])
    yellow_lower = np.array([0, 100, 100])
    yellow_upper = np.array([230, 255, 255])
    green_lower = np.array([0, 100, 0])
    green_upper = np.array([100, 255, 100])

    if np.all(
        np.logical_and(black_lower <= dominant_color, dominant_color <= black_upper)
    ):
        return "Hitam"
    elif np.all(
        np.logical_and(white_lower <= dominant_color, dominant_color <= white_upper)
    ):
        return "Putih"
    elif np.all(
        np.logical_and(red_lower <= dominant_color, dominant_color <= red_upper)
    ):
        return "Merah"
    elif np.all(
        np.logical_and(yellow_lower <= dominant_color, dominant_color <= yellow_upper)
    ):
        return "Kuning"
    elif np.all(
        np.logical_and(green_lower <= dominant_color, dominant_color <= green_upper)
    ):
        return "Hijau"
    else:
        return "Unknown"
