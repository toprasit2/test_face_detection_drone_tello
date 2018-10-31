#===================================================================================
#
# FileName: ar_checker.py
#
# Summary:  This program provides functions for checking AR markers and 
#           drowing the movie of the drone's camera
#
#===================================================================================

import drone_controller

import sys
import time
import threading
import traceback
import numpy as np
import av
import cv2.cv2 as cv2  # for avoidance of pylint error

facePath = "opencv-master/data/haarcascades/haarcascade_frontalface_default.xml"
smilePath = "opencv-master/data/haarcascades/haarcascade_smile.xml"
faceCascade = cv2.CascadeClassifier(facePath)
smileCascade = cv2.CascadeClassifier(smilePath)
eye_cascade = cv2.CascadeClassifier('opencv-master/data/haarcascades/haarcascade_eye.xml')

class ARChecker:
    __controller = None
    __dictionary_name = cv2.aruco.DICT_7X7_100
    __dictionary = cv2.aruco.getPredefinedDictionary(__dictionary_name)
    __enable = False
    __finded_ids = set([])
    __arm_t = None

    def __init__(self, controler):
        self.__controller = controler

    def initialize(self):
        pass

    def finalize(self):
        self.stop_armcheck()

    def start_armcheck(self):
        self.__enable = True
        self.__arm_t = threading.Thread(target = self.__arm_thread)
        self.__arm_t.start()

    def stop_armcheck(self):
        if self.__enable:
            self.__enable = False
            self.__arm_t.join(1)

    def get_finded_ids(self):
        return self.__finded_ids
    
    def reset_ids(self):
        self.__finded_ids = set([])

    def __arm_thread(self):
        try:
            #drone.connect()
            self.__controller.wait_for_connection(60.0)
            stream = self.__controller.get_video_stream()
            if stream == None:
                return
            container = av.open(stream)
            # skip first 300 frames
            frame_skip = 300
            while self.__enable:
                time.sleep(0.01)
                for frame in container.decode(video=0):
                    if 0 < frame_skip:
                        frame_skip = frame_skip - 1
                        continue

                    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(np.array(frame.to_image()), self.__dictionary)
                    start_time = time.time()	# elapsed time(second) from 1970/1/1 00:00;00
                    image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                    image = cv2.aruco.drawDetectedMarkers(np.array(image), corners, ids)
                    if isinstance(ids, np.ndarray) == True:
                        for id in ids:
                            self.__finded_ids.add(id[0])

                    # getting the height and the width of the loaded image
                    height = int(image.shape[0])
                    width = int(image.shape[1])
                    resized_img = cv2.resize(image,(width,height))
                    gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.1, 5)
                    # ---- Draw a rectangle around the faces
                    for (x, y, w, h) in faces:
                        cv2.rectangle(resized_img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        roi_gray = gray[y:y+h, x:x+w]
                        roi_color = resized_img[y:y+h, x:x+w]
                        smile = smileCascade.detectMultiScale( 
                            roi_gray,
                            scaleFactor= 1.7,
                            minNeighbors=22,
                            minSize=(25, 25),
                        )
                        for (sx, sy, sw, sh) in smile:
                            print ("Found", len(smile), "smiles!")
                            cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (255, 0, 0), 2)
                        
                        eyes = eye_cascade.detectMultiScale(roi_gray)
                        for (ex,ey,ew,eh) in eyes:
                            print ("Found", len(eyes), "eyes!")
                            cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0,255,0), 2)
                    cv2.imshow('Original', resized_img)
                    cv2.waitKey(1)
                    frame_skip = int((time.time() - start_time)/frame.time_base) * 2
        except Exception as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            print(ex)
        finally:
            cv2.destroyAllWindows()
