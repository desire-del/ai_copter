import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, Command
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Path to the world file
    world_file_name = 'ports.sdf'
    world_path = os.path.join(get_package_share_directory('ai_copter'), 'world', world_file_name)

    # Path to the xacro file
    xacro_file_name = 'ai_drone.xacro'
    xacro_path = os.path.join(get_package_share_directory('ai_copter'), 'urdf', xacro_file_name)
     # Declare the 'verbose' launch argument
    return LaunchDescription([
        
        # Include Gazebo launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
            )]),
            launch_arguments={'world': world_path}.items(),
        ),
        # Start robot_state_publisher to publish the robot description
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': Command(['xacro ', xacro_path])}]
        ),
        # Spawn the robot in Gazebo
        Node(
            package='ros_gz_sim',
            executable='spawn_entity.py',
            arguments=['-topic', 'robot_description', '-entity', 'ai_drone'],
            output='screen'
        )
    ])

if __name__ == '__main__':
    generate_launch_description()
