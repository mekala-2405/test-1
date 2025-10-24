# Quick Start Guide - Individual Joint Control (Windows)

This guide will help you quickly get started with individual joint control on Windows using ROS 2 Jazzy.

## Step 1: Build the Package

Open PowerShell and navigate to your workspace:

```powershell
cd C:\your_workspace_path
colcon build --packages-select open_manipulator_bringup open_manipulator_description
call install\setup.bat
```

## Step 2: Launch Gazebo Simulation

In your PowerShell terminal:

```powershell
ros2 launch open_manipulator_bringup open_manipulator_x_gazebo_individual.launch.py
```

Wait for Gazebo to fully load (about 10-15 seconds).

## Step 3: Test the Setup

### Option A: Run the Automated Demo

Open a **new PowerShell terminal**, source your workspace, and run:

```powershell
call C:\your_workspace_path\install\setup.bat
ros2 run open_manipulator_bringup test_individual_joint_control.py
```

You should see the robot move through a series of poses!

### Option B: Run the Simple Example

```powershell
call C:\your_workspace_path\install\setup.bat
ros2 run open_manipulator_bringup simple_joint_example.py
```

This will demonstrate 4 different movement patterns.

### Option C: Manual Control via Command Line

Control individual joints directly from PowerShell:

```powershell
# Move Joint 1 to 0.5 radians
ros2 topic pub --once /joint1_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.5]}"

# Move Joint 2 to -0.3 radians
ros2 topic pub --once /joint2_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [-0.3]}"

# Move all joints at once (open multiple PowerShell windows and run simultaneously):
# Window 1:
ros2 topic pub --once /joint1_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.5]}"
# Window 2:
ros2 topic pub --once /joint2_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [-0.3]}"
# Window 3:
ros2 topic pub --once /joint3_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.8]}"
# Window 4:
ros2 topic pub --once /joint4_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [-0.2]}"
```

## Step 4: Monitor Joint States

In a new PowerShell terminal:

```powershell
call C:\your_workspace_path\install\setup.bat
ros2 topic echo /joint_states
```

## Step 5: Check Active Controllers

Verify all controllers are running:

```powershell
ros2 control list_controllers
```

You should see:
- `joint1_position_controller`
- `joint2_position_controller`
- `joint3_position_controller`
- `joint4_position_controller`
- `gripper_controller`
- `joint_state_broadcaster`

## Creating Your Own Control Script

Create a new file `my_controller.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import time

class MyController(Node):
    def __init__(self):
        super().__init__('my_controller')
        
        self.joint1_pub = self.create_publisher(
            Float64MultiArray, '/joint1_position_controller/commands', 10)
        self.joint2_pub = self.create_publisher(
            Float64MultiArray, '/joint2_position_controller/commands', 10)
        self.joint3_pub = self.create_publisher(
            Float64MultiArray, '/joint3_position_controller/commands', 10)
        self.joint4_pub = self.create_publisher(
            Float64MultiArray, '/joint4_position_controller/commands', 10)
        
    def move_to(self, j1, j2, j3, j4):
        """Move all joints to specified positions (in radians)"""
        self.joint1_pub.publish(Float64MultiArray(data=[j1]))
        self.joint2_pub.publish(Float64MultiArray(data=[j2]))
        self.joint3_pub.publish(Float64MultiArray(data=[j3]))
        self.joint4_pub.publish(Float64MultiArray(data=[j4]))
        print(f'Moving to: J1={j1}, J2={j2}, J3={j3}, J4={j4}')

def main():
    rclpy.init()
    controller = MyController()
    time.sleep(2)  # Wait for connections
    
    # Your custom movements here:
    controller.move_to(0.5, -0.3, 0.8, -0.2)
    time.sleep(3)
    
    controller.move_to(0.0, 0.0, 0.0, 0.0)  # Home
    
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Run it:
```powershell
python my_controller.py
```

## Common Issues

### Issue: "No executable found"
**Solution:** Make sure you built and sourced the workspace:
```powershell
colcon build --packages-select open_manipulator_bringup
call install\setup.bat
```

### Issue: "Controller not loaded"
**Solution:** Wait 10-15 seconds after launching Gazebo before sending commands.

### Issue: Robot not moving
**Solution:** 
1. Check controllers are active: `ros2 control list_controllers`
2. Verify topics exist: `ros2 topic list | findstr controller`
3. Make sure Gazebo simulation is running (not paused)

## Next Steps

- Modify the example scripts to create custom movements
- Add sensor feedback to your control loop
- Integrate with computer vision or other ROS 2 packages
- Create complex motion sequences

For more details, see `INDIVIDUAL_JOINT_CONTROL_README.md`
