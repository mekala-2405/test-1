# Individual Joint Control for OpenManipulator-X in Gazebo

This setup allows you to control each joint of the OpenManipulator-X independently in Gazebo simulation, without using joint trajectory controllers or MoveIt.

## What Changed

- **New Controller Configuration**: Individual position controllers for each arm joint (joint1-joint4)
- **New Launch File**: `open_manipulator_x_gazebo_individual.launch.py` 
- **New URDF**: `open_manipulator_x_individual.urdf.xacro` configured for individual joint control
- **Test Scripts**: Python scripts to control joints manually or programmatically

## Setup Instructions

### 1. Build the Package

```bash
cd ~/your_workspace
colcon build --packages-select open_manipulator_bringup open_manipulator_description
source install/setup.bash
```

### 2. Launch Gazebo with Individual Joint Control

```bash
ros2 launch open_manipulator_bringup open_manipulator_x_gazebo_individual.launch.py
```

This will start:
- Gazebo simulation
- Individual position controllers for joints 1-4
- Gripper controller (unchanged)
- Joint state broadcaster

## Available Controllers

After launching, the following controllers will be active:

- `/joint1_position_controller` - Controls Joint 1 (base rotation)
- `/joint2_position_controller` - Controls Joint 2 (shoulder)
- `/joint3_position_controller` - Controls Joint 3 (elbow)
- `/joint4_position_controller` - Controls Joint 4 (wrist)
- `/gripper_controller` - Controls gripper (unchanged)

## How to Control Joints

### Option 1: Automated Demo Script

Run the test script that demonstrates moving all joints:

```bash
ros2 run open_manipulator_bringup test_individual_joint_control.py
```

This will run through a sequence of poses, controlling all joints simultaneously.

### Option 2: Manual Interactive Control

Run the manual control script (Linux/Mac only due to keyboard input):

```bash
ros2 run open_manipulator_bringup manual_joint_control.py
```

Use keyboard controls:
- `1/2` - Decrease/Increase Joint 1
- `3/4` - Decrease/Increase Joint 2
- `5/6` - Decrease/Increase Joint 3
- `7/8` - Decrease/Increase Joint 4
- `+/-` - Adjust step size
- `h` - Home position
- `q` - Quit

### Option 3: Direct Topic Publishing (Command Line)

Publish position commands directly to individual joints:

```bash
# Move Joint 1 to 0.5 radians
ros2 topic pub --once /joint1_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.5]}"

# Move Joint 2 to -0.3 radians
ros2 topic pub --once /joint2_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [-0.3]}"

# Move Joint 3 to 0.8 radians
ros2 topic pub --once /joint3_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.8]}"

# Move Joint 4 to -0.2 radians
ros2 topic pub --once /joint4_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [-0.2]}"
```

### Option 4: Python Script (Custom Control)

Create your own Python script:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class MyJointController(Node):
    def __init__(self):
        super().__init__('my_joint_controller')
        
        # Create publishers
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
        
    def move_joints(self, j1, j2, j3, j4):
        """Send position commands to all joints simultaneously."""
        msg1 = Float64MultiArray()
        msg1.data = [j1]
        self.joint1_pub.publish(msg1)
        
        msg2 = Float64MultiArray()
        msg2.data = [j2]
        self.joint2_pub.publish(msg2)
        
        msg3 = Float64MultiArray()
        msg3.data = [j3]
        self.joint3_pub.publish(msg3)
        
        msg4 = Float64MultiArray()
        msg4.data = [j4]
        self.joint4_pub.publish(msg4)

def main():
    rclpy.init()
    controller = MyJointController()
    
    # Example: Move to a specific pose
    controller.move_joints(0.5, -0.3, 0.8, -0.2)
    
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Monitoring Joint States

To see current joint positions:

```bash
ros2 topic echo /joint_states
```

## Useful Commands

### List all active controllers:
```bash
ros2 control list_controllers
```

### Check controller status:
```bash
ros2 control list_hardware_interfaces
```

### View available topics:
```bash
ros2 topic list
```

## Joint Limits

Be aware of the physical joint limits for OpenManipulator-X:
- Joint 1: ~-3.14 to 3.14 rad
- Joint 2: ~-1.57 to 1.57 rad
- Joint 3: ~-1.57 to 1.57 rad
- Joint 4: ~-1.57 to 1.57 rad

(Check URDF files for exact limits)

## Troubleshooting

### Controllers not loading:
```bash
# Check if controller manager is running
ros2 service list | grep controller_manager

# Manually spawn a controller if needed
ros2 run controller_manager spawner joint1_position_controller
```

### No response from joints:
- Make sure Gazebo is fully loaded before publishing commands
- Verify controllers are active: `ros2 control list_controllers`
- Check topic names match exactly

### Publishing not working:
- Ensure the topic name is correct (use `ros2 topic list`)
- Message format must be `Float64MultiArray` with a single value in `data` array
- Controllers need time to initialize after launch (~5-10 seconds)

## Comparison with Original Setup

**Original Setup:**
- Uses `joint_trajectory_controller` for arm
- Requires trajectory messages with waypoints
- Typically used with MoveIt for planning
- Topics: `/arm_controller/joint_trajectory`

**New Individual Control Setup:**
- Uses individual `position_controllers/JointGroupPositionController` for each joint
- Direct position commands to each joint
- No trajectory planning required
- Topics: `/joint1_position_controller/commands`, etc.

## Reverting to Original Setup

To use the original trajectory controller setup:

```bash
ros2 launch open_manipulator_bringup open_manipulator_x_gazebo.launch.py
```

## Notes

- All joints can be commanded simultaneously - just publish to all topics
- Position commands are in radians
- The gripper controller remains unchanged
- You can use both RViz and Gazebo together by uncommenting RViz in the launch file
