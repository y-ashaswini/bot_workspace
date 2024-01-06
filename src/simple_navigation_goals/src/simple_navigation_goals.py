#!/usr/bin/env python

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib import SimpleActionClient
from geometry_msgs.msg import Twist, PointStamped

class setGoal:
    def __init__(self):
        self.command = Twist()
        self.reached = False
        self.stuck = False

        self.vel_pub = rospy.Publisher('/fourbot/cmd_vel', Twist, queue_size=1)
        self.rate = rospy.Rate(10)
        self.start = rospy.Time.now().secs
        rospy.loginfo("waiting for the server...")

        # Tell the action client that we want to spin a thread by default
        self.ac = SimpleActionClient('/move_base', MoveBaseAction)


        # ps = PointStamped(point=point_wrt_kinect)
        # pose_transformed = tf2_geometry_msgs.do_transform_point(ps, transform)

        self.ac.wait_for_server()
        self.goal = MoveBaseGoal()
        self.goal.target_pose.header.frame_id = 'map'

        while self.reached == False:
            self.reset_goal()
            wait = self.ac.wait_for_result()
            if not wait:
                rospy.logerr("Action server not available!")
                rospy.signal_shutdown("Action server shutting down...")
            else:
                rospy.loginfo("Goal execution complete!")
                self.reached = True
            
        self.stop_rover()

    def reset_goal(self):
        # Send a goal to the robot to move 3 meter forward
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.header.stamp = rospy.Time.now()
        self.goal.target_pose.pose.position.x = 6.0
        self.goal.target_pose.pose.orientation.w = 1.0
        # self.goal.target_pose.pose.orientation.w = self.goal.target_pose.pose.position.w + 1.0

        rospy.loginfo("Resetting goal...")
        self.ac.send_goal(self.goal)


    def stop_rover(self):
        self.command.linear.x = 0.0
        self.command.linear.y = 0.0 
        self.command.linear.z = 0.0 
        self.command.angular.x = 0.0
        self.command.angular.y = 0.0
        self.command.angular.z = 0.0
        rospy.signal_shutdown("Shutting down rover!")
        

def main():
    setGoal()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Keyboard interrupt, shutting down")


if __name__ == "__main__":
    try:
        rospy.init_node('movebase_client')
        main()
        rospy.loginfo("Navigation function complete!")
    except rospy.ROSInterruptException:
        rospy.loginfo("ROS Exception, shutting down.")


