from dataclasses import dataclass
import cv2
from .models import MatchResult, Team, Event
import numpy as np
import json

def draw_checkmark(bottom, width, pos):
    """Gets the points for a checkmark given how far below a point the bottom is, how wide the checkmark is and the position this should also all come from."""
    (x, y) = pos
    start = pos
    start_gen = (x + width, y)
    bot = (x + bottom, y + bottom)
    top = (x + width * 2 + 2 * bottom, y - bottom)
    bot_gen = (x + bottom + width, y + bottom)
    top_gen = (x + width * 3 + 2 * bottom, y - bottom)
    mid = (x + bottom, y + bottom - width)
    mid_gen = (x + bottom + width, y + bottom - width)
    arr = np.array([start, bot, bot_gen, top_gen, top,
                   mid_gen, mid, start_gen], np.int32)
    return [arr.reshape(-1, 1, 2)]


def checkmark(frame):
    """Adds the checkmark with preset conditions to a frame."""
    cv2.fillPoly(frame, draw_checkmark(30, 6, (5, 50)), (0, 255, 0))


def get_dict_recur(data_list):
    """Takes a list of qr codes as strings, and turns it into a list of dictionaries."""
    refined_data = []
    for i in data_list:
        refined_data.append(string_to_dict(i))
    return refined_data


def string_to_dict(data):
    """Turns a string in a json format, into a dictionary."""
    return dict(json.loads(data))


def find_text_location(text_size, width):
    """Gets location to place bottom left of a centered text box."""
    return int((width - text_size) / 2)    

def run_video():
    """Runs an opencv video that scans qr codes and returns a list of the scanned strings."""
    vid = cv2.VideoCapture(0)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    final_data = ""
    data_list = []
    feedback_counter = 0
    while True:
        ret, frame = vid.read()
        if feedback_counter > 0:
            feedback_counter -= 1
            checkmark(frame)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue
        try:
            detect = cv2.QRCodeDetector()
            data, _, _ = detect.detectAndDecode(frame)
            if data:
                final_data = data
                data_list.append(final_data)
                feedback_counter = 30
        except:
            pass
        cv2.putText(frame, "Press 'q' To Exit", (find_text_location(
            268, width), int(height) - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vid.release()
    cv2.destroyAllWindows()
    return data_list


def exe():
    """Executes the needed functions and returns a list of dictionaries."""
    data = run_video()
    return get_dict_recur(data)
