from dataclasses import dataclass
import cv2
from .models import MatchResult, Team, Event
import numpy as np


def scan_data():
    data = ""
    return data

# lookup team

def draw_checkmark(bottom, width, pos):
    (x,y) = pos
    start = pos
    start_gen = (x + width, y)
    bot = (x + bottom, y + bottom)
    top = (x + width * 2 + 2 * bottom, y - bottom)
    bot_gen = (x + bottom + width, y + bottom)
    top_gen = (x + width * 3 + 2 * bottom, y - bottom)
    mid = (x + bottom, y + bottom - width)
    mid_gen = (x + bottom + width, y + bottom - width)
    # return [start, start_gen, bot, bot_gen, top, top_gen, mid, mid_gen]
    # arr = np.array([start, start_gen, bot, bot_gen, top, top_gen, mid, mid_gen], np.int32)
    arr = np.array([start, bot, bot_gen, top_gen, top, mid_gen, mid, start_gen], np.int32)
    print(arr)
    return [arr.reshape(-1, 1, 2)]

def checkmark(frame):
    cv2.fillPoly(frame, draw_checkmark(30,6,(5,50)), (0,255,0))

def process_data():
    this_event = Event.objects.get(id=event_id)
    this_team = Team.objects.get(number=team_number)

def get_dict_recur(data_list):
    refined_data = []
    for i in data_list:
        refined_data.append(get_dict(i))
    return refined_data


def get_dict(data):
    data_dict = {}
    entries = data.split(",")
    for i in entries:
        (key, value) = i.split("|")
        data_dict[key] = value
    return data_dict

def run_video():
    # test_data = "event_id|2022onwat,match_num|27,teamnum|8089,autoScore|3,autoMove|true,teleScore|27,endScore|300,endTime|27,penalty|0,tip|false,disabled|false,comment|'beans'"
    vid = cv2.VideoCapture(0)
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
                print(data)
                feedback_counter = 30
        except:
            pass
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vid.release()
    cv2.destroyAllWindows()
    return data_list


def exe():
    print(draw_checkmark(10,4,(100,100)))
    data = run_video()
    get_dict_recur(data)



