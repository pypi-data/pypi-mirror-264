#!/usr/bin/env python3
class ArtusAPI:

    def __init__(self):
        pass

    # communication setup
    def connect(self):
        return True
    def disconnect(self):
        return True
    
    # robot states
    def wake_up(self):
        print('Waking up the robot')
        return True
    def sleep(self):
        print('Putting the robot to sleep')
        return True
    def calibrate(self):
        print('Calibrating the robot')
        return True
    
    # robot control
    def set_joint_angles(self, joint_angles):
        print('Setting joint angles to:', joint_angles)
        return True
    def get_joint_angles(self):
        print ('Getting joint angles')
        joint_positions = "[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]"
        return joint_positions