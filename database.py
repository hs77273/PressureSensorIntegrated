import base64
import os

import cv2
import mysql.connector
import numpy as np
from dotenv import load_dotenv
from face_recognition import face_encodings

from log import Logger

# Load environment variables from .env file
load_dotenv()

# Set up logging
logger = Logger(module="Database Level")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Access environment variables for database configuration
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_DATABASE"),
    "use_pure": os.getenv("DB_USE_PURE", False),  # Use pure Python implementation, default to True if not provided
}


def get_passenger_data():
    data_from_db = []

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT passengerName, personImage, passengerSeat FROM passengerdetails")
        results = cursor.fetchall()

        for passenger in results:
            try:
                load_image = base64.b64decode(passenger[1])
                image_np = np.frombuffer(load_image, dtype=np.uint8)
                image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
                face_encoding = face_encodings(image)[0]

                passenger_data = {
                    "passenger_name": passenger[0],
                    "passenger_image": load_image,
                    "passenger_dataset": [passenger[0], passenger[2], face_encoding],
                }

                data_from_db.append(passenger_data)

            except Exception as e:
                logger.error(f"Error processing passenger {passenger[0]}: {e}")
    except Exception as e:
        logger.error(f"Error fetching data from the database:  {e}")
    else:
        connection.close()

    return data_from_db
