#include <ros/ros.h>                               
#include <actionlib/client/simple_action_client.h> // action Library Header File
#include <actionlib/client/terminal_state.h> // Action Goal Status Header File
#include <actionspkg/FibonacciAction.h> // FibonacciAction Action File Header


int main(int argc, char **argv) // Node Main Function 
{
    ros::init(argc, argv, "action_client");
    // Action Client Declaration (Action Name: actionspkg)
    actionlib::SimpleActionClient<actionspkg::FibonacciAction> action_client("actionspkg", true);
    
    ROS_INFO("Waiting for action server to start.");
    action_client.waitForServer(); // Wait until action server starts
    ROS_INFO("Action server started, sending goal.");
    
    actionspkg::FibonacciGoal goal; // Declare Action Goal
    goal.order = 20; // Set Action Goal (Process the Fibonacci sequence 20 times)
    action_client.sendGoal(goal); // Transmit Action Goal

    // Set action time limit (set to 30 seconds)
    bool finished_before_timeout = action_client.waitForResult(ros::Duration(30.0));

    // Process when action results are received within the time limit for achieving the action goal
    if (finished_before_timeout)
    {
        // Receive action target status value and display on screen
        actionlib::SimpleClientGoalState state = action_client.getState();
        ROS_INFO("Action finished: %s", state.toString().c_str());

    } else
        ROS_INFO("Action did not finish before timeout.");
    // If time out occurs
    // Exit
    
    return 0;
}