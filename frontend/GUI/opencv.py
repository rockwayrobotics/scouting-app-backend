from dataclasses import dataclass
import cv2
from .models import matchResult, team, event

def scan_data():
    data = ""
    return data

#lookup team
def process_data():
    this_event = event.objects.get(id=event_id)
    this_team = team.objects.get(number=team_number)

test_data = "event_id|2022onwat,match_num|27,teamnum|8089,autoScore|3,autoMove|true,teleScore|27,endScore|300,endTime|27,penalty|0,tip|false,disabled|false,comment|'beans'"
def get_dict(data):
    data_dict = {}
    entries = data.split(",")
    for i in entries:
        (key, value) = i.split("|")
        data_dict[key] = value
    return data_dict

vid = cv2.VideoCapture(0)
final_data = ""
while True:
    ret, frame = vid.read()
    detect = cv2.QRCodeDetector()
    data, _, _ = detect.detectAndDecode(frame)
    if data:
        final_data = data
        print(data)
        break
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

data_dict = get_dict(final_data)
print(data_dict)


vid.release()
cv2.destroyAllWindows()
