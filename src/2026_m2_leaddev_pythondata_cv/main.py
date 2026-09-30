import cv2
from json import load
from dataclasses import dataclass

import numpy as np

from .shapes_detector import ShapeDetector

@dataclass
class ColorRange:
    min: int
    max: int

@dataclass
class ColorTrackerSettings:
    red=ColorRange(0, 255)
    green=ColorRange(0, 255)
    blue=ColorRange(0, 255)

    @staticmethod
    def load_settings() -> ColorTrackerSettings:
        with open("color-tracker-settings.json", "r") as file:
            loaded_data: dict[str, any] = load(file)
        color_tracker = ColorTrackerSettings()
        color_tracker.red.min = loaded_data["red"]["min"]
        color_tracker.red.max = loaded_data["red"]["max"]
        color_tracker.green.min = loaded_data["green"]["min"]
        color_tracker.green.max = loaded_data["green"]["max"]
        color_tracker.blue.min = loaded_data["blue"]["min"]
        color_tracker.blue.max = loaded_data["blue"]["max"]
        return color_tracker


def track_color(frame: cv2.typing.MatLike, tracker_color: ColorTrackerSettings):
    tracker_color: ColorTrackerSettings = tracker_color

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    min_color_to_track = np.array([tracker_color.blue.min, tracker_color.green.min, tracker_color.red.min])
    max_color_to_track = np.array([tracker_color.blue.max, tracker_color.green.max, tracker_color.red.max])

    color_mask = cv2.inRange(hsv_frame, min_color_to_track, max_color_to_track)
    hsv_result_as_frame = cv2.bitwise_and(hsv_frame, hsv_frame, mask=color_mask)

    bgr_result_as_frame = cv2.cvtColor(hsv_result_as_frame, cv2.COLOR_HSV2BGR)

    return bgr_result_as_frame


# def to_int_array(data : tuple[float]):


def detect_corners(frame: cv2.typing.MatLike) -> cv2.typing.MatLike:
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray_frame, 100, 0.075, 50)

    
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(frame, (int(x), int(y)), int(5), (255, 0, 0), 1)

    for i in range(len(corners)):
        for j in range(i+1, len(corners)):
            # print(corners[i][0])
            corner1 = tuple(corners[i][0].astype(int))
            corner2 = tuple(corners[j][0].astype(int))
            color = tuple(map(lambda x: int(x), np.random.randint(0, 255, size=3)))
            cv2.line(frame, corner1, corner2, color, int(1))

def main():
    capture = cv2.VideoCapture("roaster.mp4")

    fps = capture.get(cv2.CAP_PROP_FPS)     # Récupérer le FPS avec OpenCV
    delay = int(1000/fps)                   # Délais de mise en pause
    shape_detector = ShapeDetector(circle_min_radius=0.5)

    while True:
        color_tracker = ColorTrackerSettings.load_settings()

        has_content, frame = capture.read()
        if (has_content):

            zoom=0.5
            resized_frame = cv2.resize(frame, (0, 0), fx=zoom, fy=zoom)
            # rotated_resized_frame = cv2.rotate(resized_frame, cv2.ROTATE_180)
            # fliped_resized_frame = cv2.flip(resized_frame, 1)

            # small_mirror_frame = cv2.resize(fliped_resized_frame, (0, 0), fx=zoom, fy=zoom)
            grayscale_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            # gray_frame = cv2.cvtColor(grayscale_frame, cv2.COLOR_GRAY2BGR)

            # H, W, _ = gray_frame.shape
            # # frame[100:100+gray_frame.shape[0], 100:100+gray_frame.shape[1]] = gray_frame
            # frame[100:100+H, 100:100+W] = gray_frame


            # extracted_color_frame = track_color(frame, color_tracker)

            # detect_corners(frame)

            # blur_median_frame = cv2.medianBlur(grayscale_frame, 9)
            kernel_size = 15
            kernel = (kernel_size, kernel_size)
            blur_gaussian_frame = cv2.GaussianBlur(grayscale_frame, kernel, 0)

            # Converti une image en NOIR ET BLANC (pas de gris).
            _, threshold = cv2.threshold(
                grayscale_frame, 
                127,
                255,
                cv2.THRESH_BINARY)

            contours, _ = cv2.findContours(
                threshold,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )


            for contour in contours:
                is_shape = shape_detector.is_ellipse(resized_frame, contour)


            cv2.imshow("Lecteur Vidéo OpenCV", resized_frame)
        else:
            capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if (cv2.waitKey(delay) == ord('q')):
            break
    cv2.destroyAllWindows()

if (__name__ == "__main__"):
    main()
