import time
import pygame
import pyttsx3
from helper import play_voice_text


engine = pyttsx3.init()
voices = engine.getProperty("voices")

name = "Ravi Shanker Singh"
message = f"Dear {name} Welcome to Onboard"



class WebcamApp:
    """Main class for the ICMS Dashboard application."""

    def __init__(self, root):
        self.track_last_five_frames = {}
        self.empty_skip_update_notification = 5
        self.ui_statbility = {"A1": 0, "A2": 0, "B1": 0, "B2": 0}
        self.welcome_notification = {}
    
    def update_gui(self):
        """Update the GUI based on seatbelt status."""
        empty_skip_notification = self.empty_skip_update_notification

        for seat, (name, status, color) in self.track_last_five_frames.items():
            if status == "Empty":
                self.ui_statbility[seat] += 1  # Initialize to 0 if it's None
                for key, value in self.ui_statbility.items():
                    if value == empty_skip_notification:
                        self.notification_controller.update_single_seat(seat, None, color, status)
                        self.ui_statbility[key] = 0
            else:
                self.notification_controller.update_single_seat(seat, None, color, status)
                weclome_message = f"Dear {name}, Welcome to onboard"
                incorrect_message = f"On {seat}, Wrong Passenger"
                unauthorize_message = f"Unauthorize Access"

                if color in ['yellow', 'green'] and name not in self.welcome_notification.keys():
                    self.speak(weclome_message)
                    self.welcome_notification[name] = True
                elif color == 'orange':
                    self.speak(incorrect_message)
                elif color == 'red':
                    self.speak(unauthorize_message)
        self.clear_frames()


def play_voice_mp3(mp3_file):
    """Create voice from https://www.narakeet.com/
            VOICE: Pooja
            LANGUAGE: English - Indian Accent
            SCRIPT : voice_message\text_script.txt

    Args:
        mp3_file (_type_): _description_
    """
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play()


# Example usage:
name = "Ravi Shanker Singh"
message_text = f"Dear {name}, Welcome to Onboard"
message_mp3 = "voices//Ready for Takeoff.mp3"  # Path to the MP3 file

# Play voice from text
# play_voice_text(message_text)
# Play voice from MP3 file
play_voice_mp3(message_mp3)
time.sleep(1.5)
