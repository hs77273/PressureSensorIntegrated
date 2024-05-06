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

def seat_status():
    result = {}

    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        pin_labels = {"A2": 18}

        for pin in pin_labels.values():
            GPIO.setup(pin, GPIO.IN)

        pin_states = {label: GPIO.input(pin) for label, pin in pin_labels.items()}
        result = {label: True if state == 1 else False for label, state in pin_states.items()}

        result['A1'] = True
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