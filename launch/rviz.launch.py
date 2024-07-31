import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Obtenez le répertoire de partage du package
    package_share_directory = get_package_share_directory('ai_copter')
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    # Chemin du fichier URDF
    urdf_file = os.path.join(package_share_directory, 'urdf', 'ai_drone.urdf')
    
    # Chemin du fichier RViz
    rviz_config_file = os.path.join(package_share_directory, 'rviz', 'drone_config.rviz')
    
    # Read the URDF file
    with open(urdf_file, 'r') as infp:
        robot_description = infp.read()

    return LaunchDescription([
        # Déclarer un argument de lancement pour le fichier URDF
        DeclareLaunchArgument(
            'urdf_file',
            default_value=urdf_file,
            description='URDF file to be loaded by the Robot State Publisher'
        ),

        # Déclarer un argument de lancement pour le fichier RViz
        DeclareLaunchArgument(
            'rviz_config_file',
            default_value=rviz_config_file,
            description='RViz configuration file'
        ),
        # Démarrer RViz2 avec la configuration spécifiée
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_description}],
            arguments=[LaunchConfiguration('urdf_file')]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', LaunchConfiguration('rviz_config_file')]
        ),
    ])
