#===================================================================================
#
# FileName: modeling_simpleseq.py
#
# Summary:  This program controls drone accroding to SimpleSequencer.run method commands
#
#===================================================================================
# setting library path
import sys
sys.path.append('./../lib')

# importing library
from time import sleep
import drone_controller

#===================================================================================
# SimpleSequencer class
#===================================================================================
class SimpleSequencer:
    def __init__(self, dronecontroller):
        self._framework = framework.Framework(main)
        self.dronecontroller = dronecontroller

    def initialize(self):
        # Start Drone
        self.dronecontroller.connect()
        self.dronecontroller.wait_for_connection(20.0)

    def run(self):
        # sending commands to the drone
        self.dronecontroller.takeoff()
        sleep(5)
        self.dronecontroller.down(50)
        sleep(3)
        self.dronecontroller.land()
        sleep(5)

    def stop(self):
        # Stop Drone
        self.dronecontroller.disconnect()

def main(dronecontroller, archecker, cmdrecoder, keymanager):
    ss = SimpleSequencer(dronecontroller)
    ss.initialize()
    ss.run()
    ss.stop()

#===================================================================================
# Start up
import framework
if __name__ == '__main__':
    _framework = framework.Framework(main)
    _framework.run()
