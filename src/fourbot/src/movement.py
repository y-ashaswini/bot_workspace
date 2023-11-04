#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import time

class Movement():
    def __init__(self):
        rospy.init_node('rover_move', anonymous=True)
        self.vel_pub = rospy.Publisher('/fourbot/cmd_vel', Twist, queue_size=1)
        
        self.too_close = False

        self.forward_distance_sub = rospy.Subscriber("depthcam/color/distance_opencv",String ,self.distanceCallback)
        self.command = Twist()
        self.rate = rospy.Rate(10)
        self.end = False
        rospy.on_shutdown(self.shutdownhook)


    def distanceCallback(self, data):
        if(data < 1.8):
            self.too_close = True
            self.rotate()


    def publish_cmdvel(self):
        while not self.end:
            connections = self.vel_pub.get_num_connections()
            # get the number of connections to other ROS nodes for this topic. For a Publisher, this corresponds to the number of nodes subscribing. For a Subscriber, the number of publishers.

            if connections > 0:
                self.vel_pub.publish(self.command)
                break
            else:
                self.rate.sleep()


    def shutdownhook(self):
        self.stop_rover()
        self.end = True



    def stop_rover(self):
        rospy.loginfo("Shutting down rover!")
        self.command.linear.x = 0.0 # no linear movement
        self.command.linear.y = 0.0 
        self.command.linear.z = 0.0 
        # self.command.angular.x = 0.0
        # self.command.angular.y = 0.0
        self.command.angular.z = self.command.angular.z*-1 # no angular movement
        self.publish_cmdvel() # trigger shutdown

    
    def convert_degree_rad(self, angular_speed_deg, angle_deg):
        angular_speed_rad = angular_speed_deg * 3.14 / 180
        angle_rad = angle_deg * 3.14 / 180
        return [angular_speed_rad, angle_rad]


    def forward_step(self, forward_time = 10):
        self.command.linear.x = 5
        self.command.linear.y = 2

        t0 = rospy.Time.now().secs
        t1 = t0
        while(t1 - t0 != forward_time):
            self.vel_pub.publish(self.command)            
            t1 = rospy.Time.now().secs
            self.rate.sleep()


    def forward_continuous(self):
        self.command.linear.x = 5
        self.command.linear.y = 2

        while not self.too_close:
            self.vel_pub.publish(self.command)
            self.rate.sleep()



    def rotate(self, angular_speed_deg =30, angle_deg = 30, clockwise = False):
        self.angular_speed_deg = angular_speed_deg
        self.angle_deg = angle_deg
        self.clockwise = clockwise

        self.command.linear.x = 0
        self.command.linear.y = 0
        self.command.linear.z = 0
        self.command.angular.x = 0
        self.command.angular.y = 0
        [angular_speed_rad, angle_rad] = self.convert_degree_rad(self.angular_speed_deg, self.angle_deg)

        if(self.clockwise):
            self.command.angular.z = -abs(angular_speed_rad)
        else:
            self.command.angular.z = abs(angular_speed_rad)

        # t0 = current time
        t0 = rospy.Time.now().secs

        curr_angle = 0
        
        # loop to publish the velocity estimate, current_distance = velocity * (t1 - t0)
        while(curr_angle < angle_rad):
            
            # Publish the velocity
            self.vel_pub.publish(self.command)
            
            # t1 is the current time
            t1 = rospy.Time.now().secs
            
            # Calculate current angle
            curr_angle = angular_speed_rad*(t1 - t0)

            self.rate.sleep()

        # after taking a turn, set velocity to zero to stop the robot
        self.stop_rover()


if __name__ == '__main__':
    rover_controller_obj = Movement()
    try:
        rover_controller_obj.forward_continuous()
        rover_controller_obj.stop_rover()

    except rospy.ROSInterruptException:
        pass




