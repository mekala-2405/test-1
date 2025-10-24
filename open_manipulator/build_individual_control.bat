@echo off
REM Build script for Individual Joint Control setup
REM This script builds the necessary packages for individual joint control

echo ========================================
echo Building Individual Joint Control Setup
echo ========================================
echo.

REM Check if we're in a ROS 2 workspace
if not exist "src" (
    echo ERROR: This script must be run from the root of your ROS 2 workspace
    echo Current directory: %CD%
    echo Please cd to your workspace root and try again
    pause
    exit /b 1
)

echo Building packages...
echo.

colcon build --packages-select open_manipulator_description open_manipulator_bringup

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Build successful!
    echo ========================================
    echo.
    echo To use the individual joint control:
    echo.
    echo 1. Source the workspace:
    echo    call install\setup.bat
    echo.
    echo 2. Launch Gazebo:
    echo    ros2 launch open_manipulator_bringup open_manipulator_x_gazebo_individual.launch.py
    echo.
    echo 3. In a new terminal, run test script:
    echo    call install\setup.bat
    echo    ros2 run open_manipulator_bringup simple_joint_example.py
    echo.
    echo See WINDOWS_QUICK_START.md for more information
    echo.
) else (
    echo.
    echo ========================================
    echo Build failed!
    echo ========================================
    echo Please check the error messages above
    echo.
)

pause
