#===================================================================================
#
# FileName: framework.py
#
# Summary:  This program provides the framework for Robot Challenge in APRIS 2018
#
#===================================================================================

import drone_controller
import key_manager
import cmd_recorder
import ar_checker

class Framework:
    __controller = None
    __archecker = None
    __cmdrecoder = None
    __keymanager = None
    __main = None

    # constructor
    def __init__(self, main):
        self.__main = main

    # initialize
    def initialize(self):
        self.__controller = drone_controller.DroneController()
        self.__archecker = ar_checker.ARChecker(self.__controller)
        self.__cmdrecoder = cmd_recorder.CMDRecoder()
        self.__keymanager = key_manager.KeyManager()
        self.__keymanager.initialize()

    # finalize
    def finalize(self):
        self.__archecker.stop_armcheck()
        self.__controller.disconnect()

    # entry point
    def run(self):
        # initialize
        self.initialize()
        # user program
        try:
            self.__main(self.__controller, self.__archecker, self.__cmdrecoder, self.__keymanager)
        except KeyboardInterrupt as e:
            print(e)
        except Exception as e:
            print(e)
        # finalize
        self.finalize()
        exit(1)
