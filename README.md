Great! You can include the list of dependencies in the README file under the "Prerequisites" section. Here's an updated version:

---

# ICMS Dashboard

## Overview

The ICMS Dashboard is a web-based Integrated Cabin Management System designed to monitor and manage various aspects of cabin operations on an aircraft. It provides real-time data on seat occupancy, passenger information, and seatbelt status, ensuring a secure and efficient in-flight experience.

## Features

- **Real-time Monitoring:** View live updates of seat occupancy, passenger details, and seatbelt status.
- **Face Recognition:** Utilizes facial recognition to identify passengers and assign them to their designated seats.
- **Seatbelt Status:** Monitors seatbelt usage and alerts cabin crew to any discrepancies.
- **User-Friendly Interface:** Intuitive dashboard design for easy navigation and quick access to critical information.

## Installation

### Prerequisites

- Python 3.x
- Dependencies:
  - face-recognition==1.3.0
  - mysql-connector-python==8.2.0
  - numpy==1.24.4
  - opencv-python==4.8.1.78
  - Pillow==10.1.0
  - protobuf==4.21.12
  - python-dotenv==1.0.0

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/rs62966/icms-dashboard.git
    cd icms-dashboard
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure settings:

    - Open `.env` and update the necessary configuration settings.

4. Run the application:

    ```bash
    python icms_dashboard.py
    ```

5. Opened the ICMS Dashboard.

## Usage

1. Log in with your credentials.
2. Navigate through the dashboard to access different modules.
3. Monitor real-time updates on seat occupancy, passenger information, and seatbelt status.
4. [Include any other usage instructions]


## License

This project is licensed under the [Cyient License](https://www.cyient.com/).

