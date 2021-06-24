#!/usr/bin/env python
import rospy
from std_msgs.msg import String

import time
import numpy as np

import Adafruit_PCA9685


class Servo():
    '''
    Servo class contains all functions to control additional servos
    '''

    # Define servo names
    # If desired, you can change the names here (replace all names in this file only)
    S_ONE,S_TWO,S_THREE,S_FOUR = range(0, 4)

    def __init__(self):

        # Dictionary containing the pins of all servo
        self.pins = {
            'servo': {}
        }

        # PWM characteristics
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)  # Hz

        #Number at the end is the number of connected servos
        self.servo_pwm_neutral = [None] * 4
        self.servo_pwm_range = [None] * 4
        self.angle = [None] * 4
        self.servo_pwm_degree_offset = [None] * 4
        self.servo_startup_position = [None] * 4
        self.servo_ccw_degree = [None] * 4
        self.servo_cw_degree = [None] * 4

        #Set servo pins:
        self.pins['servo'][self.S_ONE] = rospy.get_param("pin_camera_pan")
        self.pins['servo'][self.S_TWO] = rospy.get_param("pin_camera_tilt")
        # self.pins['servo'][self.S_THREE] = rospy.get_param("pin_servo_3")
        # self.pins['servo'][self.S_FOUR] = rospy.get_param("pin_servo_4")
        
        # Memory for set angle (currently not used for any function)
        # 99 is the blank starting value as it also states, that the angle should not change
        self.angle[self.S_ONE] = 99
        self.angle[self.S_TWO] = 99
        self.angle[self.S_THREE] = 99
        self.angle[self.S_FOUR] = 99        
        
        # Set variables for the GPIO motor pins
        if rospy.get_param("pin_camera_pan")  != 99:
            self.servo_pwm_neutral[self.S_ONE] = rospy.get_param("camera_pwm_neutral_pan")
            self.servo_pwm_range[self.S_ONE] = rospy.get_param("camera_pwn_range")
            # self.servo_pwm_degree_offset[self.S_ONE] = rospy.get_param("servo_pwm_center_degree_offset_1")
            # self.servo_startup_position[self.S_ONE] = rospy.get_param("servo_startup_position_1")
            # self.servo_ccw_degree[self.S_ONE] = rospy.get_param("servo_ccw_degree_1")
            # self.servo_cw_degree[self.S_ONE] = rospy.get_param("servo_cw_degree_1")

        if rospy.get_param("pin_camera_tilt")  != 99:
            self.servo_pwm_neutral[self.S_TWO] = rospy.get_param("camera_pwm_neutral_tilt")
            self.servo_pwm_range[self.S_TWO] = rospy.get_param("camera_pwn_range")
            # self.servo_pwm_degree_offset[self.S_TWO] = rospy.get_param("servo_pwm_center_degree_offset_2")
            # self.servo_startup_position[self.S_TWO] = rospy.get_param("servo_startup_position_2")
            # self.servo_ccw_degree[self.S_TWO] = rospy.get_param("servo_ccw_degree_2")
            # self.servo_cw_degree[self.S_TWO] = rospy.get_param("servo_cw_degree_2")

        # if rospy.get_param("pin_servo_3")  != 99:
        #     self.servo_pwm_neutral[self.S_THREE] = rospy.get_param("servo_pwm_neutral_3")
        #     self.servo_pwm_range[self.S_THREE] = rospy.get_param("servo_pwm_range_3")
        #     self.servo_pwm_degree_offset[self.S_THREE] = rospy.get_param("servo_pwm_center_degree_offset_3")
        #     self.servo_startup_position[self.S_THREE] = rospy.get_param("servo_startup_position_3")
        #     self.servo_ccw_degree[self.S_THREE] = rospy.get_param("servo_ccw_degree_3")
        #     self.servo_cw_degree[self.S_THREE] = rospy.get_param("servo_cw_degree_3")

        # if rospy.get_param("pin_servo_4")  != 99:
        #     self.servo_pwm_neutral[self.S_FOUR] = rospy.get_param("servo_pwm_neutral_4")
        #     self.servo_pwm_range[self.S_FOUR] = rospy.get_param("servo_pwm_range_4")
        #     self.servo_pwm_degree_offset[self.S_FOUR] = rospy.get_param("servo_pwm_center_degree_offset_4")
        #     self.servo_startup_position[self.S_FOUR] = rospy.get_param("servo_startup_position_4")
        #     self.servo_ccw_degree[self.S_FOUR] = rospy.get_param("servo_ccw_degree_4")
        #     self.servo_cw_degree[self.S_FOUR] = rospy.get_param("servo_cw_degree_4")
        
        # Set steering motors to startup position
        for servo_name, servo_pin in self.pins['servo'].items():
            if servo_pin != 99 and self.servo_startup_position[servo_name] <= 90:
                #self.pwm.set_pwm(servo_pin, 0, self.servo_pwm_neutral[servo_name])
                # duty_cycle = int(self.servo_pwm_neutral[servo_name] + self.servo_startup_position[servo_name]/90.0 * self.servo_pwm_range[servo_name] + self.servo_pwm_degree_offset[servo_name])
                duty_cycle = int(self.servo_pwm_neutral[servo_name])
                # Send duty cycle
                self.pwm.set_pwm(servo_pin, 0, duty_cycle)
                time.sleep(0.2)
            else:
                pass

    def setAngle(self, angle_command):
        # Loop through pin dictionary. The items key is the servo_name and the value the pin.
        # Send 99 as angle_command if value/angle should not be changed
        for servo_name, servo_pin in self.pins['servo'].items():
            if servo_pin != 99:
                #90 degree limit protection (does not protect from false configuration of PWM settings)
                if angle_command[servo_name] >= -90 and angle_command[servo_name] <= 90:
                    #Variable limits check set in exomy_servo_node.yaml
                    if angle_command[servo_name] >= self.servo_ccw_degree[servo_name] and angle_command[servo_name] <= self.servo_cw_degree[servo_name]:
                        # Save angle in class memory
                        self.angle[servo_name] = angle_command[servo_name]
                        
                        # Calculate necessary duty cycle
                        duty_cycle = int(self.servo_pwm_neutral[servo_name] + angle_command[servo_name]/90.0 * self.servo_pwm_range[servo_name] + self.servo_pwm_degree_offset[servo_name])
                        # Send duty cycle
                        self.pwm.set_pwm(servo_pin, 0, duty_cycle)
                    else:
                        rospy.loginfo("Servo angle exceeded variable limits - no actions!")
                elif angle_command[servo_name] == 99:
                    # 99 is the blank value that allows not to change a value
                    pass
                else:
                    rospy.loginfo("Servo angle exceeded +/- 90 degree limits - no actions to protect servo!")
            else:
                pass