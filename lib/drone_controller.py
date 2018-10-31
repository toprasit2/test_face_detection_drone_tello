#===================================================================================
#
# FileName: drone_controller.py
#
# Summary:  This program provides functions for controling the drone
#
#===================================================================================

import tellopy
import re
import time

class DroneController:
    #ex: height= 0, fly_mode=0x06, battery_percentage=76, drone_battery_left=0x0000
    __PATTERN = 'height\=\s*(\d+), fly_mode\=\s*(0x[0-9a-fA-F]{2}), battery_percentage\=\s*(\d+), drone_battery_left\=\s*(0x[0-9a-fA-F]{4})'
    __drone :tellopy.Tello = None
    __condition = 0
    __flight_data_text = ''
    __height = 0
    __fly_mode = 0x00
    __battery_percentage = 0
    __drone_battery_left = 0x0000

    def initialize(self):
        pass

    def finalize(self):
        self.disconnect()

    def connect(self):
        if  self.__drone == None:
            self.__drone = tellopy.Tello()
            self.__drone.video_encoder_rate = 1
            self.__drone.connect()
            self.__drone.start_video()
            # getting sensor data event handler
            def handler(event, sender, data, **args):
                drone = sender
                if event is drone.EVENT_FLIGHT_DATA:
                    self.__flight_data_text = str(data)
                    result = re.match(self.__PATTERN, self.__flight_data_text)
                    self.__height = int(result.group(1))
                    self.__fly_mode = int(result.group(2), 0)
                    self.__battery_percentage = int(result.group(3))
                    self.__drone_battery_left = int(result.group(4), 0)
            self.__drone.subscribe(self.__drone.EVENT_FLIGHT_DATA, handler)
            #self.drone.subscribe(self.__drone.EVENT_VIDEO_FRAME, __handler)

    def disconnect(self):
        if  self.__drone != None:
            self.land()
            self.__drone.quit()
            self.__drone = None

    def get_condition(self):
        return self.__condition

    def wait_for_connection(self, sec):
        if self.__drone != None:
            self.__drone.wait_for_connection(sec)

    def get_video_stream(self):
        if self.__drone != None:
            return self.__drone.get_video_stream()
        else:
            return None

    def get_flight_data(self):
        return self.__flight_data_text

    def get_height(self):
        return self.__height

    def get_fly_mode(self):
        return self.__fly_mode

    def get_battery_percentage(self):
        return self.__battery_percentage

    def get_drone_battery_left(self):
        return self.__drone_battery_left

    def takeoff(self):
        if self.__condition == 0:
            self.__drone.takeoff()
            time.sleep(5)
            self.__condition = 1

    def land(self):
        if self.__condition == 1:
            self.__drone.down(50)
            time.sleep(5)
            self.__drone.land()
            self.__condition = 0

    def forward(self, val):
        if self.__condition == 1:
            self.__drone.forward(val)

    def backward(self, val):
        if self.__condition == 1:
            self.__drone.backward(val)

    def right(self, val):
        if self.__condition == 1:
            self.__drone.right(val)

    def left(self, val):
        if self.__condition == 1:
            self.__drone.left(val)

    def clockwise(self, val):
        if self.__condition == 1:
            self.__drone.clockwise(val)

    def counter_clockwise(self, val):
        if self.__condition == 1:
            self.__drone.counter_clockwise(val)

    def up(self, val):
        if self.__condition == 1:
            self.__drone.up(val)

    def down(self, val):
        if self.__condition == 1:
            self.__drone.down(val)

    def stop(self):
        self.forward(0)
        self.left(0)
        self.clockwise(0)
