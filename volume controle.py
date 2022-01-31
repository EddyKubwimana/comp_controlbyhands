import math
import time
from ctypes import cast, POINTER

import cv2
import numpy as np
from comtypes import CLSCTX_ALL
from cvzone.HandTrackingModule import HandDetector
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
vol = volume.GetVolumeRange()
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMute()
volume.GetMasterVolumeLevel()
volume.GetVolumeRange()
minvol = vol[0]
maxvol = vol[1]
vid = cv2.VideoCapture(0)
vid.set(3, 1300)
vid.set(4, 800)
detector = HandDetector(maxHands=2, detectionCon=0.8)
ptime = 0
volbar = 0
while True:
    success, img = vid.read()
    Hands, img = detector.findHands(img)
    if Hands:
        Hand1 = Hands[0]
        lmlist = Hand1['lmList']
        if lmlist:
            _, info, img = detector.findDistance(lmlist[8], lmlist[4], img)
            dist, _, img = detector.findDistance(lmlist[8], lmlist[12], img)
            x1, y1 = lmlist[4]
            x2, y2 = lmlist[8]
            lenght = math.sqrt(((x2 - x1) ** 2) + (y2 - y1) ** 2)
            vo = np.interp(lenght, [30, 300], [minvol, maxvol])
            volbar = np.interp(lenght, [30, 300], [400, 100])
            percentvo = np.interp(lenght, [30, 300], [0, 100])
            if dist >= 100:
                cv2.putText(img, f'{int(percentvo)}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                volume.SetMasterVolumeLevel(vo, None)
                cv2.rectangle(img, (50, 100), (1, 400), (0, 255, 0), 2)
                cv2.rectangle(img, (50, int(volbar)), (1, 400), (0, 255, 0), cv2.FILLED)
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, f'fps: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv2.imshow("image", img)
    cv2.waitKey(1)
