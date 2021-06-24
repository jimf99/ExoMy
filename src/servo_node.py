#!/usr/bin/env python
import time
import rospy

from exomy.msg import ServoCommands
from servo import Servo

servo = Servo()
global watchdog_timer


def callback(cmds):
    servo.setAngle(cmds.servo_angles)

if __name__ == "__main__":
    # This node waits for commands from the robot and sets the motors accordingly
    rospy.init_node("motors")
    rospy.loginfo("Starting the servo node")

    sub = rospy.Subscriber(
        "/servo_commands", ServoCommands, callback, queue_size=1)

    rate = rospy.Rate(10)

    rospy.spin()
