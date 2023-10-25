#include <ros/ros.h>                               
#include <actionlib/server/simple_action_server.h> // action Library Header File
#include <actionspkg/FibonacciAction.h>  // FibonacciAction Action File Header

class FibonacciAction
{
protected:
    ros::NodeHandle nh;
    actionlib::SimpleActionServer<actionspkg::FibonacciAction> action_server;
    std::string action_name;
    actionspkg::FibonacciFeedback feedback;
    actionspkg::FibonacciResult result;

public:
    // Initialize action server (Node handle, action name, action callback function)
    FibonacciAction(std::string name) : action_server(nh, name, boost::bind(&FibonacciAction::executeCB, this, _1), false), action_name(name)
    {
        action_server.start();
    }
    ~FibonacciAction(void) {} // destructor?
    
    // A function that receives an action goal message and performs a specified action (in this example, a Fibonacci calculation).
    // What is CB
    void executeCB(const actionspkg::FibonacciGoalConstPtr &goal)
    {
        ros::Rate r(1); // Loop Rate: 1Hz
        bool success = true; // Used as a variable to store the success or failure of an action


        // Setting Fibonacci sequence initialization,
        // add first (0) and second message (1) of feedback.
        feedback.sequence.clear();
        feedback.sequence.push_back(0);
        feedback.sequence.push_back(1);
        // feedback sequence is now: [0, 1]

        // Notify the user of action name, goal, initial two values of Fibonacci sequence
        ROS_INFO("%s: Executing, creating fibonacci sequence of order %i with seeds %i, %i", action_name.c_str(), goal->order, feedback.sequence[0], feedback.sequence[1]);


        // Action content
        for (int i = 1; i <= goal->order; i++)
        {
            // Confirm action cancellation from action client
            if (action_server.isPreemptRequested() || !ros::ok())
            {
                // NOTICE: isPreemptRequested() : meaning external interrupt from user : meaning cancellation request!
                // Notify action cancellation
                ROS_INFO("%s: Preempted", action_name.c_str());
                action_server.setPreempted(); // Action cancellation
                success = false;    // Consider action as failure and save to variable
                break;
            }

            // Store the sum of current Fibonacci number and the previous number in the feedback
            // while there is no action cancellation or the action target value is reached.
            feedback.sequence.push_back(feedback.sequence[i] + feedback.sequence[i - 1]);
            action_server.publishFeedback(feedback); // Publish feedback
            r.sleep(); // sleep according to the defined loop rate.

        }
        
        // If the action target value is reached, transmit current Fibonacci sequence as the result value.
        if (success) {
            result.sequence = feedback.sequence;
            ROS_INFO("%s: Succeeded", action_name.c_str());
            action_server.setSucceeded(result);
        }

    }
};


int main(int argc, char **argv){
    ros::init(argc, argv, "action_server");
    FibonacciAction fibonacci("actionspkg");
    ros::spin();
    return 0;
}