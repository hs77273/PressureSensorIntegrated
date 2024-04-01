#!/bin/bash


# Set the base directory and password
# SUDO_PASSWORD=""
# BASE_DIR="/home/cyient/Desktop/ICMS/Icms_Dashboard"

# # Define the path to your Python script
# FOLDER_PATH='$BASE_DIR/ICMS/'
# PYTHON_SCRIPT='icms_dashboard.py'
# if [ $# -eq 1 ]; then
# 	PYTHON_SCRIPT=$1
# fi					
# echo "Runing $PYTHON_SCRIPT..."
# # Run the Python script with sudo, providing the password
# echo "$SUDO_PASSWORD" | sudo -S "$BASE_DIR/venv/bin/python" "$FOLDER_PATH/$PYTHON_SCRIPT"


# Set the base directory and password
SUDO_PASSWORD=""
BASE_DIR="$(dirname "$0")"  # Assuming the script is in the same directory
PYTHON_SCRIPT='icms_dashboard.py'

if [ $# -eq 1 ]; then
    PYTHON_SCRIPT=$1
fi

LOG_FILE="$BASE_DIR/icms.log"

echo "Running $PYTHON_SCRIPT..." | tee -a "$LOG_FILE"

# Run the Python script with sudo, providing the password
echo "$SUDO_PASSWORD" | sudo -S "$BASE_DIR/venv/bin/python" "$BASE_DIR/ICMS/$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "Script executed successfully."
else
    echo "Error: Script execution failed."
fi
