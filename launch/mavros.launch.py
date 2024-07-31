import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='mavros',
            executable='mavros_node',
            output='screen',
            parameters=[
                {'fcu_url': 'udp://:14540@localhost:14557'},
                {'gcs_url': 'udp://@localhost:14550'},
                {'target_system_id': 1},
                {'target_component_id': 1}
            ]
        )
    ])
