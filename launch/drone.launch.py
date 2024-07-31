import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node


def generate_launch_description():
    # Configure ROS nodes for launch

    # Setup project paths
    pkg_project_bringup = get_package_share_directory('ai_copter')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Chemin du fichier Xacro
    xacro_file = os.path.join(pkg_project_bringup, 'urdf', 'ai_drone.xacro')

    # Chemin du fichier RViz
    rviz_config_file = os.path.join(pkg_project_bringup, 'config', 'drone.rviz')

    # Setup to launch the simulator and Gazebo world
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': PathJoinSubstitution([
            pkg_project_bringup,
            'world',
            'ports.sdf'
        ])}.items(),
    )

    # Takes the description and joint angles as inputs and publishes the 3D poses of the robot links
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': Command(['xacro ', xacro_file])},
        ]
    )

    # Visualize in RViz
    rviz = Node(
       package='rviz2',
       executable='rviz2',
       arguments=['-d', rviz_config_file],
       condition=IfCondition(LaunchConfiguration('rviz')),
    )

    # Bridge between ROS 2 and Gazebo
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': os.path.join(pkg_project_bringup, 'config', 'ros_gz_bridge.yaml'),
            'qos_overrides./tf_static.publisher.durability': 'transient_local',
        }],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'rviz',
            default_value='true',
            description='Open RViz.'
        ),
        gz_sim,
        bridge,
        robot_state_publisher,
        rviz
    ])
