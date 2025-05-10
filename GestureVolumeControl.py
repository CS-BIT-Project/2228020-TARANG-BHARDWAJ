import cv2
import math
import time
import HandTracingModule as htm
import numpy as np
import osascript
import subprocess

#################################################
wCam, hCam = 1200, 680
#################################################
cap= cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)


def get_mute_status():
    # Get the mute status
    script = "output muted of (get volume settings)"
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return result.stdout.strip() == "true"

def get_master_volume_level():
    # Get the current volume level
    script = "output volume of (get volume settings)"
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return int(result.stdout.strip())

def get_volume_range():
    # macOS does not have a defined volume range like Windows, but we can assume 0 to 100
    return (0, 100)

def set_master_volume_level(level):
    # Set the volume level (0 to 100)
    if 0 <= level <= 100:
        script = f"set volume output volume {level}"
        subprocess.run(['osascript', '-e', script])

# Example usage
is_muted = get_mute_status()
current_volume = get_master_volume_level()
volume_range = get_volume_range()

# print(f"Is Muted: {is_muted}")
# print(f"Current Volume: {current_volume}")
# print(f"Volume Range: {volume_range}")

# Set volume to 0%

minVol = volume_range[0]
maxVol= volume_range[1]
pTime = 0
detector = htm.handDetector(detectionCon=0.7)
vol=0
volPer=0
volBar=300
while True:
    sucess, img = cap. read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList) != 0:
        # print(lmList[4],lmList[8])
        x1, y1 = lmList[4][1],lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx,cy= (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2),(255, 0, 0),2)
        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        # to find the length of the line
        length= math.hypot(x2-x1, y2-y1)
        print(length)


        # Hand Range was form 30 to 400
        # Volume range is from 0 to 100
        vol =np.interp(length,[30,300],[minVol, maxVol])
        volBar = np.interp(length, [30, 300], [300,130])
        volPer = np.interp(length, [30, 300], [0, 100])
        print(int(length),vol)
        set_master_volume_level(vol)

        if length<30:
            cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)

    cv2.rectangle(img,(50,100),(85,400),(229,204,255),3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (229,204,255), cv2.FILLED)
    cv2.putText(img, f'FPS: {int(volPer)} %', (10, 470), cv2.FONT_ITALIC, 1,
                (229,204,255), 2)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}' , (10, 70), cv2.FONT_ITALIC, 1,
                (225, 154, 192), 2)

    cv2.imshow("Img",img)
    cv2.waitKey(2)