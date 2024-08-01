# Autonomous UAV for ship inspection

## Requirements

### System Requirements

* [ROS Humble](https://docs.ros.org/en/humble/Installation.html)

* [Gazebo Garden](https://gazebosim.org/docs/garden/install)

* [Cartographer ROS](https://google-cartographer-ros.readthedocs.io/en/latest/)


### Workspace Requirements

* [Ardupilot](https://github.com/ArduPilot/ardupilot_gz)

* [Ros 2]()

* [Gazebo]()

## Installation

### Setup workspace
Follow this youtube tutorial for setup the workspace: ![youtube](https://www.youtube.com/watch?v=2BhyKyzKAbM&ab_channel=XiaodiTao)

### Install ai_copter package

```bash
cd ~/ros2_ws/src
git clone 

```

## Build

Build it with colcon build:
```bash
cd ~/ros2_ws
colcon build --packages-select ai_copter

```

## Usage

### 1. Launch Gazebo and Rviz

This simulation has an Iris copter equipped with camera in a port world.
To launch rviz and gazebo, run:

```bash
cd ~/ros2_ws
source install/setup.bash
ros2 launch ai_copter drone_camera.launch.py
```
In another terminal, with the world and copter in place, Mavproxy:

```bash
cd ~/ros2_ws
source install/setup.bash
mavproxy.py --console --aircraft test --master :14550

```