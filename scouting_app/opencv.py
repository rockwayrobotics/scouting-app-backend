from dataclasses import dataclass
import cv2
from .models import MatchResult, Team, Event
import numpy as np
import json
import time

data_base = {}

def gen_key():
    return int(time.time())

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

def find_text_location(text_size, width):
    """Gets location to place bottom left of a centered text box."""
    return int((width - text_size) / 2)


def switch_mode(mode):
    """Deals with the logic of switching modes and defining keystrokes to their modes."""
    mode_dict = {
        ord("d") : default_mode,
        ord("c") : comment_mode,
        ord("q") : quit_cam,
        ord("a") : adv,
    }
    if mode & 0xFF in mode_dict:
        return mode_dict[mode]
    else:
        return None

def base_mode(vid, feedback_counter, frame_cmds, dimension):
    """The function that deals with the logic of processing a frame and executing the mode that the program is currently in on that frame."""
    cmd = frame_cmds
    key = cv2.waitKey(33)
    _, frame = vid.read()
    cv2.putText(frame, "Press 'q' To Exit", (find_text_location(
        268, dimension[0]), int(dimension[1]) - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
    new_cmd = switch_mode(key)
    if new_cmd:
        cmd = [new_cmd]
    if feedback_counter > 0:
        feedback_counter -= 1
        checkmark(frame)
    else:
        for command in cmd:
            feedback_counter = command(frame)
    cv2.imshow('frame', frame)
    return (feedback_counter, cmd)

def default_mode(frame):
    """Default mode that scans QR Codes and puts them in the dictionary."""
    feedback_counter = 0
    try:
        detect = cv2.QRCodeDetector()
        data, _, _ = detect.detectAndDecode(frame)
        if data:
            # print("data gotten")
            data_base[gen_key()] = data
            feedback_counter = 30
    except:
        pass
    return feedback_counter

def adv(frame):
    """Currently Not Developed"""
    return

def quit_cam(frame):
    """Quits the camera and returns the dictionary of everything scanned so far."""
    return

def get_sorted_keys():
    """Gets the keys of a dictionary and sorts them."""
    return sorted(list(data_base.keys()))

def comment_mode(frame):
    """Scans QR Codes and adds a comment section if a comment QR code is scanned to the latest match details."""
    feedback_counter = 0
    try:
        detect = cv2.QRCodeDetector()
        data, _, _ = detect.detectAndDecode(frame)
        if data:
            if data[:6] == "cmmnt|":
                keys = get_sorted_keys()
                for i in keys:
                    if "stat" in data_base[i]:
                        data_base[i]["comment"] = data[6:]
                        break
            else:
                key = gen_key()
                data_base[key] = {"stat" : data}   
            feedback_counter = 30
    except:
        pass
    return feedback_counter


def run_video():
    """Runs an opencv video that scans qr codes and returns a list of the scanned strings."""
    vid = cv2.VideoCapture(0)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    dimension = (width, height)
    feedback_counter = 0
    cmd = [default_mode]
    while True:
        (feedback_counter, cmd) = base_mode(vid, feedback_counter, cmd, dimension)
        if cmd == [quit_cam]:
            break
    vid.release()
    cv2.destroyAllWindows()


def exe():
    """Executes the needed functions and returns a list of dictionaries."""
    run_video()
    print(data_base)
    return data_base
