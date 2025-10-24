#!/usr/bin/env python3
"""
Manual individual joint control tool for OpenManipulator-X.
Allows interactive control of each joint from command line.

Usage:
    ros2 run open_manipulator_bringup manual_joint_control.py
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import sys
import termios
import tty


class ManualJointController(Node):
    def __init__(self):
        super().__init__('manual_joint_controller')
        
        # Publishers for each joint
        self.joint1_pub = self.create_publisher(
            Float64MultiArray, '/joint1_position_controller/commands', 10
        )
        self.joint2_pub = self.create_publisher(
            Float64MultiArray, '/joint2_position_controller/commands', 10
        )
        self.joint3_pub = self.create_publisher(
            Float64MultiArray, '/joint3_position_controller/commands', 10
        )
        self.joint4_pub = self.create_publisher(
            Float64MultiArray, '/joint4_position_controller/commands', 10
        )
        
        # Current joint positions
        self.joint_positions = [0.0, 0.0, 0.0, 0.0]
        self.step_size = 0.1  # radians
        
        self.get_logger().info('Manual Joint Controller started!')
        self.print_help()
        
    def print_help(self):
        """Print control instructions."""
        print("\n" + "="*60)
        print("OpenManipulator-X Manual Joint Control")
        print("="*60)
        print("\nControls:")
        print("  1/2 - Decrease/Increase Joint 1 (Base rotation)")
        print("  3/4 - Decrease/Increase Joint 2 (Shoulder)")
        print("  5/6 - Decrease/Increase Joint 3 (Elbow)")
        print("  7/8 - Decrease/Increase Joint 4 (Wrist)")
        print("\n  +/- - Increase/Decrease step size")
        print("  h   - Go to home position (all zeros)")
        print("  p   - Print current positions")
        print("  ?   - Show this help")
        print("  q   - Quit")
        print("="*60)
        print(f"\nCurrent step size: {self.step_size:.3f} radians")
        self.print_positions()
        print()
        
    def print_positions(self):
        """Print current joint positions."""
        print(f"\nCurrent positions (radians):")
        print(f"  Joint 1: {self.joint_positions[0]:6.3f}")
        print(f"  Joint 2: {self.joint_positions[1]:6.3f}")
        print(f"  Joint 3: {self.joint_positions[2]:6.3f}")
        print(f"  Joint 4: {self.joint_positions[3]:6.3f}")
        
    def send_joint_command(self, joint_idx, position):
        """Send command to specific joint."""
        msg = Float64MultiArray()
        msg.data = [position]
        
        publishers = [self.joint1_pub, self.joint2_pub, 
                     self.joint3_pub, self.joint4_pub]
        
        publishers[joint_idx].publish(msg)
        
    def update_joint(self, joint_idx, delta):
        """Update joint position and publish."""
        self.joint_positions[joint_idx] += delta
        self.send_joint_command(joint_idx, self.joint_positions[joint_idx])
        self.get_logger().info(
            f'Joint {joint_idx+1}: {self.joint_positions[joint_idx]:.3f} rad'
        )
        
    def go_home(self):
        """Send all joints to home position."""
        self.joint_positions = [0.0, 0.0, 0.0, 0.0]
        for i in range(4):
            self.send_joint_command(i, 0.0)
        self.get_logger().info('Going to home position')
        self.print_positions()
        
    def handle_key(self, key):
        """Handle keyboard input."""
        if key == '1':
            self.update_joint(0, -self.step_size)
        elif key == '2':
            self.update_joint(0, self.step_size)
        elif key == '3':
            self.update_joint(1, -self.step_size)
        elif key == '4':
            self.update_joint(1, self.step_size)
        elif key == '5':
            self.update_joint(2, -self.step_size)
        elif key == '6':
            self.update_joint(2, self.step_size)
        elif key == '7':
            self.update_joint(3, -self.step_size)
        elif key == '8':
            self.update_joint(3, self.step_size)
        elif key == '+' or key == '=':
            self.step_size = min(0.5, self.step_size + 0.05)
            print(f"Step size: {self.step_size:.3f} rad")
        elif key == '-':
            self.step_size = max(0.01, self.step_size - 0.05)
            print(f"Step size: {self.step_size:.3f} rad")
        elif key == 'h' or key == 'H':
            self.go_home()
        elif key == 'p' or key == 'P':
            self.print_positions()
        elif key == '?' or key == '/':
            self.print_help()
        elif key == 'q' or key == 'Q':
            return False
        return True


def get_key():
    """Get a single keypress from the user (Linux/Mac)."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key


def main(args=None):
    rclpy.init(args=args)
    controller = ManualJointController()
    
    try:
        import time
        time.sleep(1)  # Wait for publishers to connect
        
        while True:
            key = get_key()
            if not controller.handle_key(key):
                break
                
    except KeyboardInterrupt:
        pass
    except Exception as e:
        controller.get_logger().error(f'Error: {e}')
    finally:
        controller.get_logger().info('Shutting down...')
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
