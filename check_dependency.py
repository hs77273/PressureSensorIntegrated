import json
import os
import pathlib
import platform
import re

import cv2
import pkg_resources

from database import get_passenger_data
from log import Logger
from seatbelt import seatbelt_status

logger = Logger(module="Check ICMS Dependency")


def print_separator():
    logger.info("*" * 30)


def check_camera():
    try:
        current = pathlib.Path(__file__).parent.resolve()
        with open(current.joinpath("config.json")) as data_file:
            data = json.load(data_file)

        camera_source_1 = data["CAMERA"]["FIRST_CAMERA_INDEX"]
        camera_source_2 = data["CAMERA"]["SECOND_CAMERA_INDEX"]

        for camera_source in [camera_source_1, camera_source_2]:
            cap = cv2.VideoCapture(camera_source)
            if not cap.isOpened():
                logger.warn(f"Error: Camera source {camera_source} is not available.")
            else:
                logger.info(f"Camera source {camera_source} is available.")
                cap.release()

    except Exception as e:
        logger.error(f"Error checking camera devices: {e}")


def check_db():
    connection = None
    logger.info("🗄️  DB Status:")
    try:
        database = get_passenger_data()
        logger.info(f"Successfully connected to the database and read passenger {len(database)}.")
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def check_platform():
    logger.info("💻🖱️ Platform Info:")
    current_platform = platform.system()
    if current_platform.lower() == "linux" and os.uname().machine.startswith("aarch64"):
        logger.info("It's a Jetson platform: {}".format(current_platform))
    else:
        logger.error(f"It's a {current_platform} platform.")


def check_installation(requirements_file=None):
    if requirements_file:
        logger.info("🚀 Checking and installing required packages...")
        with open(requirements_file, "r") as f:
            required_packages = [line.strip().split("#")[0].strip() for line in f.readlines()]
        installed_packages = [package.key for package in pkg_resources.working_set]

        missing_packages = []
        for package in required_packages:
            if not package:  # Skip empty lines
                continue
            package_name = re.split("[<>=@ ]+", package.strip())[0]
            if package_name.lower() not in installed_packages:
                missing_packages.append(package_name)

        if missing_packages:
            logger.info(f"Missing packages: {', '.join(missing_packages)}")
            # sys.exit(1)
        else:
            logger.info("✅ All packages are installed.")
    else:
        logger.info("please provide requirements file")


def check_belt_read():
    try:
        seat_belt_status = seatbelt_status()
        logger.info("✅ Seat belt Sensor Working fine")
    except Exception as e:
        logger.warn("❌ Seat belt Sensor Not Working")


def main():
    file = "./requirements.txt"
    check_installation(file)
    print_separator()
    check_camera()
    print_separator()
    check_platform()
    print_separator()
    check_belt_read()
    print_separator()
    check_db()


if __name__ == "__main__":
    main()
