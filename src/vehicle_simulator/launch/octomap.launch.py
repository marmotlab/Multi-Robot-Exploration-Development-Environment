import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    base_frame = LaunchConfiguration('base_frame')
    sensor_range = LaunchConfiguration('sensor_range')
    map_resolution = LaunchConfiguration('map_resolution')
    namespace = LaunchConfiguration('namespace')

    return LaunchDescription([
        DeclareLaunchArgument(
            'base_frame', default_value='sensor',
            description='Base frame id'
        ),
        DeclareLaunchArgument(
            'sensor_range', default_value='20.0',
            description='Sensor range (m)'
        ),
        DeclareLaunchArgument(
            'map_resolution', default_value='0.4',
            description='Map resolution (m)'
        ),
        DeclareLaunchArgument(
            'namespace', default_value='robot_0',
            description='robot id'
        ),

        Node(
            package='octomap_server',
            executable='octomap_server_node',
            name='octomap',
            namespace=namespace, 
            output='screen',
            remappings=[('cloud_in', 'sensor_scan')],
            parameters=[{
                'frame_id': "map",
                'base_frame_id': [namespace, '/', base_frame],
                'resolution': map_resolution,

                'occupancy_min_z': 0.5,
                'occupancy_max_z': 1.2,

                'sensor_model.max_range': sensor_range,
                'sensor_model.hit': 1.0,
                'sensor_model.miss': 0.45,
                'sensor_model.max': 1.0,
                'sensor_model.min': 0.2,     

                'publish_2d_map': True,
                'compress_map': True,
            }]
        ),
        
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='link_broadcaster',
            arguments=['0', '0', '0', '0', '0', '0', '1', [namespace, TextSubstitution(text='/vehicle')], 
                       [namespace, TextSubstitution(text='/base_link')]]
        ),

    ])
