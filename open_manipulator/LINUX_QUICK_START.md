# Linux Quick Start Guide - Individual Joint Control

This guide is for running the individual joint control setup on a Linux system with ROS 2 Jazzy.

## Prerequisites

- ROS 2 Jazzy installed on Linux
- Gazebo (gz-sim) installed
- OpenManipulator packages in your workspace

## Step-by-Step Instructions

### Step 1: Transfer Files to Linux System

Transfer your entire `open_manipulator` folder to your Linux workspace:

```bash
# On your Linux system, navigate to your ROS 2 workspace
cd ~/ros2_ws/src  # or wherever your workspace is

# If transferring via git:
git clone <your-repo-url>

# Or if copying from Windows, the new files you need are:
# - open_manipulator_bringup/config/open_manipulator_x/individual_joint_controllers.yaml
# - open_manipulator_bringup/launch/open_manipulator_x_gazebo_individual.launch.py
# - open_manipulator_bringup/open_manipulator_bringup/test_individual_joint_control.py
# - open_manipulator_bringup/open_manipulator_bringup/simple_joint_example.py
# - open_manipulator_bringup/open_manipulator_bringup/manual_joint_control.py
# - open_manipulator_description/urdf/open_manipulator_x/open_manipulator_x_individual.urdf.xacro
# - Modified setup.py
```

### Step 2: Build the Workspace

```bash
cd ~/ros2_ws  # Go to workspace root
colcon build --packages-select open_manipulator_description open_manipulator_bringup
source install/setup.bash
```

### Step 3: Launch Gazebo Simulation

Open Terminal 1:
```bash
source ~/ros2_ws/install/setup.bash
ros2 launch open_manipulator_bringup open_manipulator_x_gazebo_individual.launch.py
```

**Wait 10-15 seconds** for Gazebo to fully load and controllers to initialize.

### Step 4: Test the Setup

Open Terminal 2 and choose one test method:

#### Option A: Simple Automated Example (Recommended First Test)
```bash
source ~/ros2_ws/install/setup.bash
ros2 run open_manipulator_bringup simple_joint_example.py
```

You should see the robot move through 4 different movement patterns.

#### Option B: Full Demo Sequence
```bash
source ~/ros2_ws/install/setup.bash
ros2 run open_manipulator_bringup test_individual_joint_control.py
```

#### Option C: Interactive Manual Control (Linux Only - Best!)
```bash
source ~/ros2_ws/install/setup.bash
ros2 run open_manipulator_bringup manual_joint_control.py
```

**Keyboard Controls:**
- `1` / `2` - Decrease/Increase Joint 1 (base rotation)
- `3` / `4` - Decrease/Increase Joint 2 (shoulder)
- `5` / `6` - Decrease/Increase Joint 3 (elbow)
- `7` / `8` - Decrease/Increase Joint 4 (wrist)
- `+` / `-` - Increase/Decrease step size
- `h` - Go to home position (all zeros)
- `p` - Print current positions
- `?` - Show help
- `q` - Quit

#### Option D: Command Line Direct Control
```bash
# Move individual joints:
ros2 topic pub --once /joint1_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.5]}"
ros2 topic pub --once /joint2_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [-0.3]}"
ros2 topic pub --once /joint3_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.8]}"
ros2 topic pub --once /joint4_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [-0.2]}"

# Move all joints simultaneously (using background processes):
ros2 topic pub --once /joint1_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.5]}" &
ros2 topic pub --once /joint2_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [-0.3]}" &
ros2 topic pub --once /joint3_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.8]}" &
ros2 topic pub --once /joint4_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [-0.2]}"
```

### Step 5: Verify Everything Works

Open Terminal 3:

```bash
source ~/ros2_ws/install/setup.bash

# Check controllers are active:
ros2 control list_controllers
```

**Expected Output:**
```
joint1_position_controller[position_controllers/JointGroupPositionController] active
joint2_position_controller[position_controllers/JointGroupPositionController] active
joint3_position_controller[position_controllers/JointGroupPositionController] active
joint4_position_controller[position_controllers/JointGroupPositionController] active
gripper_controller[position_controllers/GripperActionController] active
joint_state_broadcaster[joint_state_broadcaster/JointStateBroadcaster] active
```

```bash
# List all control topics:
ros2 topic list | grep controller

# Monitor joint states:
ros2 topic echo /joint_states
```

## Available Control Topics

| Topic | Message Type | Description |
|-------|-------------|-------------|
| `/joint1_position_controller/commands` | Float64MultiArray | Joint 1 (base rotation) |
| `/joint2_position_controller/commands` | Float64MultiArray | Joint 2 (shoulder) |
| `/joint3_position_controller/commands` | Float64MultiArray | Joint 3 (elbow) |
| `/joint4_position_controller/commands` | Float64MultiArray | Joint 4 (wrist) |
| `/joint_states` | JointState | Read current positions |

## Writing Your Own Control Script

Create a file `my_controller.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import time
import math

class MyController(Node):
    def __init__(self):
        super().__init__('my_controller')
        
        # Create publishers for each joint
        self.joint1_pub = self.create_publisher(
            Float64MultiArray, '/joint1_position_controller/commands', 10)
        self.joint2_pub = self.create_publisher(
            Float64MultiArray, '/joint2_position_controller/commands', 10)
        self.joint3_pub = self.create_publisher(
            Float64MultiArray, '/joint3_position_controller/commands', 10)
        self.joint4_pub = self.create_publisher(
            Float64MultiArray, '/joint4_position_controller/commands', 10)
        
        self.get_logger().info('My Controller initialized!')
        
    def move_to(self, j1, j2, j3, j4):
        """Move all joints to specified positions (radians)"""
        self.joint1_pub.publish(Float64MultiArray(data=[j1]))
        self.joint2_pub.publish(Float64MultiArray(data=[j2]))
        self.joint3_pub.publish(Float64MultiArray(data=[j3]))
        self.joint4_pub.publish(Float64MultiArray(data=[j4]))
        self.get_logger().info(f'Moving to: J1={j1:.3f}, J2={j2:.3f}, J3={j3:.3f}, J4={j4:.3f}')

def main():
    rclpy.init()
    controller = MyController()
    
    time.sleep(2)  # Wait for publishers to connect
    
    # Your custom movements:
    controller.move_to(0.0, 0.0, 0.0, 0.0)  # Home
    time.sleep(3)
    
    controller.move_to(0.5, -0.3, 0.8, -0.2)  # Custom pose
    time.sleep(3)
    
    controller.move_to(0.0, 0.0, 0.0, 0.0)  # Return home
    
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Make it executable and run:
```bash
chmod +x my_controller.py
python3 my_controller.py
```

## Quick Command Reference

```bash
# Build
cd ~/ros2_ws
colcon build --packages-select open_manipulator_description open_manipulator_bringup
source install/setup.bash

# Launch Gazebo
ros2 launch open_manipulator_bringup open_manipulator_x_gazebo_individual.launch.py

# Test (new terminal)
source ~/ros2_ws/install/setup.bash
ros2 run open_manipulator_bringup simple_joint_example.py

# Interactive control
ros2 run open_manipulator_bringup manual_joint_control.py

# Check controllers
ros2 control list_controllers

# Monitor joints
ros2 topic echo /joint_states

# Direct control
ros2 topic pub --once /joint1_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.5]}"
```

## Troubleshooting

### Issue: Controllers not loading
```bash
# Check controller manager is running:
ros2 service list | grep controller_manager

# Manually spawn controller if needed:
ros2 run controller_manager spawner joint1_position_controller
```

### Issue: Robot not moving
1. Wait 10-15 seconds after launch before sending commands
2. Check controllers are active: `ros2 control list_controllers`
3. Verify Gazebo is running (not paused)
4. Check topics exist: `ros2 topic list | grep controller`

### Issue: Python script not found
```bash
# Rebuild with correct packages:
cd ~/ros2_ws
colcon build --packages-select open_manipulator_bringup --symlink-install
source install/setup.bash
```

### Issue: Permission denied on Python scripts
```bash
chmod +x ~/ros2_ws/install/open_manipulator_bringup/lib/open_manipulator_bringup/*.py
```

## Key Features

✅ **No Joint Trajectory Controller** - Uses simple position controllers
✅ **No MoveIt** - Direct position commands
✅ **Individual Control** - Each joint has its own topic
✅ **Simultaneous Control** - Command all joints at once
✅ **Interactive Control** - Keyboard control available (Linux only)
✅ **Simple API** - Just publish Float64MultiArray messages

## Important Notes

- **Positions are in RADIANS** (not degrees)
- All 4 joints can be controlled simultaneously
- The gripper controller remains unchanged from original setup
- Joint limits are defined in the URDF - check before commanding extreme values
- Controllers take ~5-10 seconds to fully initialize after launch

## Monitoring & Debugging

```bash
# View all topics:
ros2 topic list

# View topic info:
ros2 topic info /joint1_position_controller/commands

# View message type:
ros2 interface show std_msgs/msg/Float64MultiArray

# Echo specific joint commands being sent:
ros2 topic echo /joint1_position_controller/commands

# View TF tree:
ros2 run tf2_tools view_frames

# RQT for visualization:
rqt
```

## Original Setup Still Available

The original joint trajectory controller setup is still available:
```bash
ros2 launch open_manipulator_bringup open_manipulator_x_gazebo.launch.py
```

This uses the original trajectory controller and is compatible with MoveIt.

## Additional Resources

- See `INDIVIDUAL_JOINT_CONTROL_README.md` for complete documentation
- See `CHANGES_SUMMARY.md` for what changed
- See example scripts in `open_manipulator_bringup/open_manipulator_bringup/`

## ROS 2 Dependencies

Make sure these packages are installed:
```bash
sudo apt install ros-jazzy-ros2-control
sudo apt install ros-jazzy-ros2-controllers
sudo apt install ros-jazzy-gazebo-ros2-control
sudo apt install ros-jazzy-position-controllers
```
