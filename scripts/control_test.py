#! /usr/bin/env python3

import rospy
from std_msgs.msg import Float64
import curses
from time import sleep
import numpy as np

WHEEL_RADIUS = 0.5

def radToKmh(rads):
    return 3.6 * WHEEL_RADIUS * rads

if __name__ == "__main__":
    # Create publishers for gas and steering
    gas_pub = rospy.Publisher("/gogoro/gas/command", Float64, queue_size=1)
    steering_pub = rospy.Publisher("/gogoro/steering/command", Float64, 
            queue_size=1)

    rospy.init_node("gogoro_control_test", anonymous=True)

    rate = rospy.Rate(30)

    forward_speed = 0.0
    steering_pos = 0.0

    SPEED_INC = 10.0
    STEERING_INC = np.radians(30)

    # Prepare a curses window control
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    while not rospy.is_shutdown():
        stdscr.clear()

        kmh_speed = radToKmh(forward_speed)
        stdscr.addstr(f"Speed: {forward_speed:.2f} rad/s | {kmh_speed:.2f} km/h \n")
        stdscr.addstr(f"Angle: {steering_pos:.2f} | {np.degrees(steering_pos):.2f}")

        c = stdscr.getch()
        if c == ord('a'):
            steering_pos += STEERING_INC
        elif c == ord('d'):
            steering_pos -= STEERING_INC
        elif c == ord('w'):
            forward_speed += SPEED_INC
        elif c == ord('s'):
            forward_speed -= SPEED_INC
        elif c == ord('q'):
            break

        #stdscr.refresh()
        sleep(0.033)
        gas_pub.publish(forward_speed)
        steering_pub.publish(steering_pos)
        #rate.sleep()

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    print("Finished.")

