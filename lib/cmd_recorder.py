#===================================================================================
#
# FileName: cmd_recorder.py
#
# Summary:  This program provides functions for recording drone commands by csv format.
#
#===================================================================================

import datetime
import csv

class CMDRecoder:
    __save_cmdList = []

    def write_csv(self, filename):
        write_f = open(filename, 'w', newline='')             # create csv file
        writer = csv.writer(write_f, delimiter=',')
        print(self.__save_cmdList)
        save_count = len(self.__save_cmdList)
        i = 0
        while i < save_count:
            print(self.__save_cmdList[i])
            writer.writerow(self.__save_cmdList[i]) 
            i += 1
        write_f.close()

    def save_cmd(self, cmds):
        dt = datetime.datetime.now()
        minute = dt.minute
        second = dt.second
        micro=dt.microsecond
        micro_time = minute * 60 * 1000000 + second * 1000000 + micro
        self.__save_cmdList.append([micro_time, cmds])
