import platform

from log import Logger

if platform.machine() == "aarch64":  # Checking if the platform is Jetson
    try:
        import Jetson.GPIO as GPIO
    except ModuleNotFoundError:
        GPIO = None
else:
    GPIO = None

logger = Logger("SeltBelt Sensor Module")


def seatbelt_status():
    """Get Seat Belt Status.
    pin_labels = {'A1': 31, 'A2': 7, 'B1': 33, 'B2': 29}
    Reference colour code:: {'A1': YELLOW, 'A2': BLUE, 'B1': RED, 'B2': GREEN}

    Returns:
        dict: Dictionary containing seat belt status for each label.
              False indicates 'No Belt', True indicates 'Belt'.
    """
    result = {}

    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        pin_labels = {"A1": 31, "A2": 7, "B1": 33, "B2": 29}

        for pin in pin_labels.values():
            GPIO.setup(pin, GPIO.IN)

        pin_states = {label: GPIO.input(pin) for label, pin in pin_labels.items()}
        result = {label: True if state == GPIO.HIGH else False for label, state in pin_states.items()}

    except GPIO.GPIOException as gpio_ex:
        logger.warn(f"GPIO Exception in seatbelt_status: {gpio_ex}")
    except Exception as e:
        logger.warn(f"Error in seatbelt_status: {e}")
    finally:
        GPIO.cleanup()

    return result

call_count = 0

# def seat_status():
#     global call_count
#     call_count += 1
#     seats = {"A1": True, "A2": True, "B1": True, "B2": True}
#     if call_count >= 10 and call_count < 20:
#         seats["B2"] = False
#     elif call_count >= 30 and call_count < 40:
#         seats["B2"] = True
#     elif call_count >= 40:
#         seats["A1"] = False
#         seats["A2"] = False
#         seats["B1"] = False
#         seats["B2"] = False
#     return seats

# def seat_status():
#     return {"A1": True, "A2": False, "B1": True, "B2": True}

def seat_status():
    result = {}

    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        pin_labels = {"A1": 13}

        for pin in pin_labels.values():
            GPIO.setup(pin, GPIO.IN)

        pin_states = {label: GPIO.input(pin) for label, pin in pin_labels.items()}
        result = {label: True if state == 1 else False for label, state in pin_states.items()}

        result['A2'] = True
        result['B1'] = True
        result['B2'] = True

    except GPIO.GPIOException as gpio_ex:
        print(f"GPIO Exception in seatbelt_status: {gpio_ex}")
    except Exception as e:
        print(f"Error in seatbelt_status: {e}")
    finally:
        if GPIO is not None:
            GPIO.cleanup()
    
    return result