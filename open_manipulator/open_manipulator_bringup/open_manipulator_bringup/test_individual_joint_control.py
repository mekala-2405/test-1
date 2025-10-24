#!/usr/bin/env python3
"""
Test script for individual joint control of OpenManipulator-X in Gazebo.
This script allows you to send position commands to each joint independently.

Usage:
    ros2 run open_manipulator_bringup test_individual_joint_control.py

Controls:
    - Send individual joint positions via topics
    - All joints can be controlled simultaneously
    - Gripper remains on its original controller
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import math
import time


class IndividualJointController(Node):
    def __init__(self):
        super().__init__('individual_joint_controller')
        
        # Publishers for each joint
        self.joint1_pub = self.create_publisher(
            Float64MultiArray, 
            '/joint1_position_controller/commands', 
            10
        )
        self.joint2_pub = self.create_publisher(
            Float64MultiArray, 
            '/joint2_position_controller/commands', 
            10
        )
        self.joint3_pub = self.create_publisher(
            Float64MultiArray, 
            '/joint3_position_controller/commands', 
            10
        )
        self.joint4_pub = self.create_publisher(
            Float64MultiArray, 
            '/joint4_position_controller/commands', 
            10
        )
        
        self.get_logger().info('Individual Joint Controller initialized!')
        self.get_logger().info('Publishing to:')
        self.get_logger().info('  - /joint1_position_controller/commands')
        self.get_logger().info('  - /joint2_position_controller/commands')
        self.get_logger().info('  - /joint3_position_controller/commands')
        self.get_logger().info('  - /joint4_position_controller/commands')
        
    def send_joint_positions(self, j1, j2, j3, j4):
        """
        Send position commands to all joints simultaneously.
        
        Args:
            j1, j2, j3, j4: Joint positions in radians
        """
        msg1 = Float64MultiArray()
        msg1.data = [j1]
        
        msg2 = Float64MultiArray()
        msg2.data = [j2]
        
        msg3 = Float64MultiArray()
        msg3.data = [j3]
        
        msg4 = Float64MultiArray()
        msg4.data = [j4]
        
        # Publish all commands simultaneously
        self.joint1_pub.publish(msg1)
        self.joint2_pub.publish(msg2)
        self.joint3_pub.publish(msg3)
        self.joint4_pub.publish(msg4)
        
        self.get_logger().info(
            f'Sent positions: J1={j1:.3f}, J2={j2:.3f}, J3={j3:.3f}, J4={j4:.3f}'
        )
    
    def run_demo(self):
        """
        Run a demo sequence showing different joint movements.
        """
        self.get_logger().info('Starting demo sequence...')
        time.sleep(2)  # Wait for connections
        
        # Define demo poses
        poses = [
            {
                'name': 'Home Position',
                'joints': [0.0, 0.0, 0.0, 0.0]
            },
            {
                'name': 'Joint 1 rotation',
                'joints': [math.pi/4, 0.0, 0.0, 0.0]
            },
            {
                'name': 'Joint 2 bend',
                'joints': [math.pi/4, -math.pi/6, 0.0, 0.0]
            },
            {
                'name': 'Joint 3 bend',
                'joints': [math.pi/4, -math.pi/6, math.pi/6, 0.0]
            },
            {
                'name': 'Joint 4 rotation',
                'joints': [math.pi/4, -math.pi/6, math.pi/6, math.pi/4]
            },
            {
                'name': 'All joints move',
                'joints': [0.0, -math.pi/4, math.pi/3, -math.pi/4]
            },
            {
                'name': 'Return to Home',
                'joints': [0.0, 0.0, 0.0, 0.0]
            },
        ]
        
        for pose in poses:
            self.get_logger().info(f'\n--- {pose["name"]} ---')
            self.send_joint_positions(*pose['joints'])
            time.sleep(3)  # Wait between poses
        
        self.get_logger().info('\nDemo complete!')


def main(args=None):
    rclpy.init(args=args)
    
    controller = IndividualJointController()
    
    try:
        # Run the demo
        controller.run_demo()
        
        # Keep node alive for manual control if needed
        # You can publish to the topics manually while this runs
        rclpy.spin(controller)
        
    except KeyboardInterrupt:
        controller.get_logger().info('Shutting down...')
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
