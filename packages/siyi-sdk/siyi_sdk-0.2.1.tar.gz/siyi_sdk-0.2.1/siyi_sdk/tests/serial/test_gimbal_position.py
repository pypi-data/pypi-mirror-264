"""
@file test_gimbal_rotation.py
@Description: This is a test script for using the SIYI SDK Python implementation to set/get gimbal rotation
@Author: Mohamed Abdelkader
@Contact: mohamedashraf123@gmail.com
All rights reserved 2022
"""

from time import sleep
import sys
import os
  
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
  
sys.path.append(parent_directory)

from siyi_sdk import SIYISDK

def test():
    cam = SIYISDK(communication_mode='serial', serial_port='/dev/serial0', baudrate=115200, debug=True)
    if not cam.connect():
        print("No connection ")
        exit(1)

    cam.requestGimbalPosition(110,25)
    #sleep(5)
    #print("Attitude (yaw,pitch,roll) eg:", cam.getAttitude())
    
    cam.disconnect()

if __name__ == "__main__":
    test()