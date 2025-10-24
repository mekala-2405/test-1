#!/usr/bin/env python3
"""
Simple example: Control all joints simultaneously with predefined positions.
This example sends commands to all 4 joints at the same time.

Usage:
    ros2 run open_manipulator_bringup simple_joint_example.py
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import time
import math


class SimpleJointExample(Node):
    def __init__(self):
        super().__init__('simple_joint_example')
        
        # Create publishers for each joint
        self.publishers = {
            'joint1': self.create_publisher(Float64MultiArray, '/joint1_position_controller/commands', 10),
            'joint2': self.create_publisher(Float64MultiArray, '/joint2_position_controller/commands', 10),
            'joint3': self.create_publisher(Float64MultiArray, '/joint3_position_controller/commands', 10),
            'joint4': self.create_publisher(Float64MultiArray, '/joint4_position_controller/commands', 10),
        }
        
        self.get_logger().info('Simple Joint Example Node initialized!')
        
    def send_positions(self, positions):
        """
        Send position commands to all joints.
        
        Args:
            positions: dict with keys 'joint1' through 'joint4' and values in radians
        """
        for joint_name, position in positions.items():
            msg = Float64MultiArray()
            msg.data = [position]
            self.publishers[joint_name].publish(msg)
        
        self.get_logger().info(f'Sent positions: {positions}')


def main(args=None):
    rclpy.init(args=args)
    node = SimpleJointExample()
    
    # Wait for connections to establish
    time.sleep(2)
    
    print("\n" + "="*60)
    print("Simple Joint Control Example")
    print("="*60 + "\n")
    
    # Example 1: Move all joints to specific positions
    print("Example 1: Moving all joints simultaneously to custom positions...")
    node.send_positions({
        'joint1': 0.5,      # 0.5 radians (~28.6 degrees)
        'joint2': -0.3,     # -0.3 radians (~-17.2 degrees)
        'joint3': 0.8,      # 0.8 radians (~45.8 degrees)
        'joint4': -0.2      # -0.2 radians (~-11.5 degrees)
    })
    time.sleep(3)
    
    # Example 2: Different pose
    print("\nExample 2: Moving to another pose...")
    node.send_positions({
        'joint1': -0.5,
        'joint2': 0.5,
        'joint3': -0.5,
        'joint4': 0.5
    })
    time.sleep(3)
    
    # Example 3: Return to home position
    print("\nExample 3: Returning to home position (all zeros)...")
    node.send_positions({
        'joint1': 0.0,
        'joint2': 0.0,
        'joint3': 0.0,
        'joint4': 0.0
    })
    time.sleep(3)
    
    # Example 4: Wave motion (sinusoidal)
    print("\nExample 4: Wave motion with Joint 1...")
    for i in range(20):
        angle = math.sin(i * 0.3) * 0.5  # Oscillate between -0.5 and 0.5 rad
        node.send_positions({
            'joint1': angle,
            'joint2': 0.0,
            'joint3': 0.0,
            'joint4': 0.0
        })
        time.sleep(0.2)
    
    print("\nExample complete!")
    print("="*60 + "\n")
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
