import json
import os
import pathlib

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import os
import pathlib
import time

import cv2
import numpy as np
from face_recognition import face_locations
from keras.models import load_model

from CameraAccess import create_webcam_stream
from helper import draw_seats, seats_coordinates
from log import Logger

# Set up logging
logger = Logger("Test Coordinate")
current = pathlib.Path(__file__).parent.resolve()


with open(current.joinpath("config.json")) as data_file:
    data = json.load(data_file)
    camera_source_1 = data["CAMERA"]["FIRST_CAMERA_INDEX"]
    camera_source_2 = data["CAMERA"]["SECOND_CAMERA_INDEX"]
    two_cam_seat_coordinates = seats_coordinates(data["SEAT_COORDINATES"], data["FRAME_SHAPE"])


model_file = current.joinpath("model", "keras_model.h5")
class_names = ["Seat Belt", "No Seat Belt"]
model = load_model(model_file, compile=False)

class_names = ["Seat Belt", "No Seat Belt"]

# fmt: off
def seat_belt_process(frame):
    image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
    image = (image / 127.5) - 1
    prediction = model.predict(image.reshape(1, 224, 224, 3), verbose=0)
    index = np.argmax(prediction)
    label_name = class_names[index]
    confidence_score = prediction[0][index]
    return label_name, confidence_score

# fmt: off
def process_seatbelt(frame, seat_coordinate):
    for x1, y1, x2, y2, seat_name in seat_coordinate:
        try:
            seat = frame[y2:y1, x1:x2]
            class_name, confidence_score = seat_belt_process(seat)
            label = f" {seat_name} ::  {class_name}: {round(confidence_score * 100, 2)}%"
            cv2.putText(frame, label, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        except Exception as e:
            logger.error("Error in process_seatbelt:: {e}")

    return frame

# fmt: off
def process_faces(frame, seat_coordinates):
    for (x1, y1, x2, y2, name) in seat_coordinates:
        seat_roi = frame[y2:y1, x1:x2]
        face_areas = face_locations(seat_roi)

        for face_location in face_areas:
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (x1 + left, y2 + top), (x1 + right, y2 + bottom), (255, 0, 0), 2)
            cv2.putText(frame, f"Face in Seat {name}", (x1 + left, y2 + top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 1, cv2.LINE_AA)

    return frame

# fmt: off
def main(face_detection=True, seat_belt_detection=False):
    width, height = 1800, 900
    frame_time = 1
    frame_process = 0
    seat_coordinates =two_cam_seat_coordinates
    video_capture = create_webcam_stream(camera_source_1,camera_source_2)
    video_capture.start()

    prev_frame_time = 0

    try:
        if video_capture.stopped:
            logger.error("[Exiting]: Error accessing webcam stream.")
            return
        
        while not video_capture.stopped:
            frame = video_capture.read()
            if frame is not None:
                frame_process += 1
                frame = draw_seats(frame, seat_coordinates)
                if seat_belt_detection:
                    frame = process_seatbelt(frame, seat_coordinates)
                if face_detection:
                    frame = process_faces(frame, seat_coordinates)

                new_frame_time = time.time()
                fps = 1 / (new_frame_time - prev_frame_time)
                prev_frame_time = new_frame_time

                fps_text = f"FPS: {fps:.2f}"
                cv2.putText(frame, fps_text, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

                cv2.imshow("Video", frame)

            if cv2.waitKey(frame_time) & 0xFF == ord("q"):
                video_capture.stop()
                break

    except Exception as e:
        logger.error(f"Error in process_seatbelt {e}")


if __name__ == "__main__":
    main()
