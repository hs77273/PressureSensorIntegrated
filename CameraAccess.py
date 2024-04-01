import platform
from threading import Thread

import cv2

from log import Logger

# Set up logging
logger = Logger("WebcamStream")


class WebcamStream:
    def __init__(self, stream_id=0):
        self.stream_id = stream_id
        if platform.system() == "Windows":
            self.vcap = cv2.VideoCapture(stream_id, cv2.CAP_DSHOW)
        else:
            self.vcap = cv2.VideoCapture(stream_id)

        self.grabbed, self.frame = self.vcap.read()

        if self.grabbed is False and self.vcap.isOpened() is False:
            logger.error(f"[Exiting] No more frames to read camera index {stream_id}")
            exit(0)

        self.stopped = True
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True

    def start(self):
        self.stopped = False
        self.t.start()

    def update(self):
        while True:
            if self.stopped is True:
                break
            self.grabbed, self.frame = self.vcap.read()
            if self.grabbed is False:
                logger.warn("[Exiting] No more frames to read")
                self.stopped = True
                break
        self.vcap.release()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True


class DualWebcamStream:
    def __init__(self, stream_id1=0, stream_id2=1):
        self.stopped = True
        self.stream1 = WebcamStream(stream_id1)
        self.stream2 = WebcamStream(stream_id2)

    def start(self):
        self.stopped = False
        self.stream1.start()
        self.stream2.start()

    def read(self):
        frame1 = self.stream1.read()
        frame2 = self.stream2.read()

        if frame1 is not None and frame2 is not None:
            combined_frame = cv2.hconcat([frame1, frame2])
            return combined_frame
        else:
            return None

    def stop(self):
        self.stream1.stop()
        self.stream2.stop()
        self.stopped = True


def create_webcam_stream(*args):
    num_cameras = len(args)
    if num_cameras == 1:
        return WebcamStream(args[0])
    elif num_cameras == 2:
        return DualWebcamStream(args[0], args[1])
    else:
        raise logger.warn("You can provide one or two camera IDs only.")


# Example usage:
# single_stream = create_webcam_stream(0)
# dual_stream = create_webcam_stream(0, 1)
